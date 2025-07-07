#!/bin/bash
# Start the FastAPI server on port 3001 with uvicorn in production mode

exec uvicorn src.api.main:app --host 0.0.0.0 --port 3001
