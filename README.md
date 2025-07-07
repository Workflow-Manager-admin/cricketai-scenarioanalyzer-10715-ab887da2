f# cricketai-scenarioanalyzer-10715-ab887da2

## Python Backend Setup

### Running with Docker

1. Build the Docker image:
   ```bash
   cd python_backend
   docker build -t cricketai-backend .
   ```

2. Run the container:
   ```bash
   docker run -p 3001:3001 cricketai-backend
   ```

### Running Locally without Docker

1. Install dependencies:
   ```bash
   cd python_backend
   pip install -r requirements.txt
   ```

2. Start the backend:
   ```bash
   ./start.sh
   ```

The FastAPI server will be available at http://localhost:3001
