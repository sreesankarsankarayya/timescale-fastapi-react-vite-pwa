# FastAPI React Vite PWA Timeseries Dashboard

This project is a full-stack application that combines a FastAPI backend with a React Vite Progressive Web App (PWA) frontend. It demonstrates the following features:

- **Real-time Data Streaming:**  
  A background service generates random timeseries data and stores it in a PostgreSQL database enhanced with TimescaleDB hypertables.

- **WebSocket Communication:**  
  The backend broadcasts live data over a WebSocket endpoint for the frontend to visualize using a running chart.

- **Modern Frontend Stack:**  
  The React PWA is built using TypeScript (TSX), Vite, and styled with Tailwind CSS.

- **Docker & Docker Compose:**  
  The entire codebase, including the backend, frontend, and PostgreSQL with TimescaleDB, is containerized and orchestrated via Docker Compose.

---

## Demo

Below is a recording demonstrating the working of the page and backend logs, showing data generation and live graph updates on the UI.

![Demo GIF](.assets/FastAPi_ReactTSVitePWA_Timescale_WS.gif)
<!-- Replace "path/to/your-demo.gif" with the actual path or URL to your GIF file -->

---

## Table of Contents

- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [Starting the Services](#starting-the-services)
  - [Endpoints](#endpoints)
- [Development](#development)
- [Tagging and Versioning](#tagging-and-versioning)
- [License](#license)

---

## Getting Started

### Prerequisites

- **Docker & Docker Compose:**  
  Ensure you have Docker and Docker Compose installed on your machine.  
  [Get Docker](https://docs.docker.com/get-docker/) | [Get Docker Compose](https://docs.docker.com/compose/install/)

- **Git:**  
  Version control is managed with Git.

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/sreesankarsankarayya/timescale-fastapi-react-vite-pwa.git
   cd timescale-fastapi-react-vite-pwa.git
   cd code
   ```

2. **Build and Start the Containers:**

   Use Docker Compose to build the images and start the containers:

   ```bash
   docker compose up --build
   ```

   > **Note:** If you are using Docker Compose v2, you can use `docker compose` instead of `docker-compose`.

3. **Verify Services:**

   - **Backend:**  
     The FastAPI backend will be accessible at [http://localhost:8000](http://localhost:8000).

   - **Frontend:**  
     The React PWA is served from the backend. Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## Project Structure

```
code\.
├── backend
│   ├── main.py                # FastAPI backend application
│   ├── requirements.txt       # Python dependencies
├── frontend
│   ├── public
│   │   └── manifest.json      # PWA manifest file
│   ├── src
│   │   ├── App.tsx            # Main React component (includes the chart)
│   │   └── main.tsx           # React entry point
│   ├── index.html             # HTML template
│   ├── vite.config.ts         # Vite configuration
│   ├── package.json           # Frontend dependencies and scripts
│   ├── tsconfig.json          # TypeScript configuration
│   └── tailwind.config.js     # Tailwind CSS configuration
├── Dockerfile                 # Multi-stage Docker build for backend and frontend
└── docker-compose.yml         # Docker Compose configuration
```

---

## Usage

### Starting the Services

After running `docker compose up --build`:

1. **Access the App:**  
   Open your browser and go to [http://localhost:8000](http://localhost:8000).

2. **Control Data Generation:**  
   - Click **Start Data Generation** to begin streaming random timeseries data.
   - Click **Stop Data Generation** to halt the data stream.

3. **Real-time Chart:**  
   The frontend uses a WebSocket connection to receive live data updates and renders a running chart using Chart.js.

### Endpoints

- **POST `/start`**  
  Starts the random data generation and broadcasting process.

- **POST `/stop`**  
  Stops the data generation process.

- **WebSocket `/ws/timeseries`**  
  Streams real-time timeseries data to connected clients.

---

## Development

### Running Locally Without Docker

If you wish to run the backend or frontend separately for development, install the respective dependencies:

- **Backend:**

  ```bash
  cd backend
  pip install -r requirements.txt
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```

- **Frontend:**

  ```bash
  cd frontend
  npm install
  npm run dev
  ```

  > **Note:** When running separately, ensure that the WebSocket URL in your frontend code points to the correct backend address (e.g., `ws://localhost:8000/ws/timeseries`).

### Rebuilding and Restarting with Docker

If you make changes and need to rebuild your Docker images:

```bash
docker compose up --build
```

---

## Tagging and Versioning

When you’re ready to tag this version in Git:

1. **Add and Commit Changes:**

   ```bash
   git add .
   git commit -m "Initial version with FastAPI, React Vite PWA, and TimescaleDB"
   ```

2. **Tag the Release:**

   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   ```

3. **Push Tags to Remote:**

   ```bash
   git push origin --tags
   ```

---

## License

This project is licensed under the [MIT License](LICENSE).
