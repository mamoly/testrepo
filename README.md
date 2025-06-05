# Shogi App

This repository contains a minimal prototype of a web-based shogi application.
It consists of a Python backend using FastAPI and a simple Angular frontend.
The focus is real-time online play with game data stored in files.

## Backend

The backend exposes a small REST API. Games are stored as JSON under
`backend/games/`. To run the API server:

```bash
pip install fastapi uvicorn pydantic
uvicorn backend.main:app --reload
```

## Frontend

A minimal Angular skeleton lives in `frontend/`. Install dependencies and start
the dev server:

```bash
cd frontend
npm install
yarn start  # or npm start
```

The frontend does not implement full gameplay but demonstrates how to connect
to the backend.
