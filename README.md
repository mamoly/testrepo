# Shogi App

This project provides a simple web based shogi application.  A Python FastAPI
backend stores game data as JSON files and an Angular frontend displays a board
and lets you move pieces.

## Backend

Install dependencies and run the API server:

```bash
pip install fastapi uvicorn pydantic
uvicorn backend.main:app --reload
```

The server stores games under `backend/games/`.  The following endpoints are
available:

- `POST /game` – create a new game.  Provide allocations for pieces in the
  request body.  Returns a `game_id`.
- `GET /game/{game_id}` – fetch the current game state.
- `POST /game/{game_id}/move` – make a move with from/to coordinates.
- `GET /games` – list saved games.

## Frontend

The frontend is an Angular application.  Install dependencies and start the dev
server:

```bash
cd frontend
npm install
npm start
```

Visit `http://localhost:4200` to open the app.  Click **Start Game** to create a
new game.  The board will be shown as a 9×9 grid.  Click a piece and then use
the inputs to specify a target square.

This is not a full implementation of shogi rules but provides a working base
for testing and further development.
