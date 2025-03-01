import asyncio
import datetime
import logging
import os
import random
import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Column, DateTime, Float, Integer, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database URL (using the environment variable set by docker-compose)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@db:5432/postgres")

# Create async engine and session maker
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Define SQLAlchemy base and model
Base = declarative_base()

from sqlalchemy import Column, DateTime, Float, Integer, PrimaryKeyConstraint
import datetime

class TimeSeries(Base):
    __tablename__ = "timeseries"
    id = Column(Integer, autoincrement=True)
    ts = Column(DateTime, default=datetime.datetime.utcnow)
    value = Column(Float)
    __table_args__ = (PrimaryKeyConstraint("ts", "id"),)

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files from the built frontend (copied into ./static)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

# Global set for connected websocket clients and streaming task handle
connected_websockets = set()
streaming_task = None

async def wait_for_db(retries: int = 10, delay: int = 2):
    for attempt in range(1, retries + 1):
        try:
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("Database connection established.")
            return
        except OperationalError as e:
            logger.error(f"Database not ready (attempt {attempt}/{retries}): {e}")
            await asyncio.sleep(delay)
    raise Exception("Could not connect to the database after several attempts.")

@app.on_event("startup")
async def startup_event():
    # Wait for the DB to be ready
    await wait_for_db()

    # Create tables (if not already created) and the hypertable
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created.")
        # Convert the table into a hypertable (TimescaleDB function)
        await conn.execute(text("SELECT create_hypertable('timeseries', 'ts', if_not_exists => TRUE);"))
        logger.info("Hypertable ensured.")

@app.websocket("/ws/timeseries")
async def websocket_endpoint(websocket: WebSocket):
    origin = websocket.headers.get("origin")
    logger.info(f"WebSocket connection attempt from origin: {origin}")
    await websocket.accept()
    connected_websockets.add(websocket)
    try:
        while True:
            await asyncio.sleep(3600)
    except WebSocketDisconnect:
        connected_websockets.remove(websocket)
        logger.info("WebSocket client disconnected.")

async def broadcast_data(message: str):
    """Send message to all connected websocket clients."""
    for websocket in list(connected_websockets):
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending to websocket: {e}")
            connected_websockets.remove(websocket)

async def generate_data():
    """Continuously generate random timeseries data, save to DB, and broadcast via websocket."""
    while True:
        new_value = random.random() * 100
        new_ts = datetime.datetime.utcnow()
        data_str = f"{new_ts.isoformat()},{new_value}"
        logger.info(f"Generated data: {data_str}")
        async with async_session() as session:
            async with session.begin():
                record = TimeSeries(ts=new_ts, value=new_value)
                session.add(record)
        await broadcast_data(data_str)
        await asyncio.sleep(1)

@app.post("/start")
async def start_generation():
    """Endpoint to start the random data generator."""
    global streaming_task
    if streaming_task is None or streaming_task.done():
        streaming_task = asyncio.create_task(generate_data())
        logger.info("Started data generation.")
        return {"status": "Data generation started."}
    else:
        return {"status": "Data generation already running."}

@app.post("/stop")
async def stop_generation():
    """Endpoint to stop the random data generator."""
    global streaming_task
    if streaming_task and not streaming_task.done():
        streaming_task.cancel()
        logger.info("Stopped data generation.")
        return {"status": "Data generation stopped."}
    else:
        return {"status": "No data generation running."}

