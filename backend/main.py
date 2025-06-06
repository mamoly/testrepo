from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
import uuid
import json
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'games')
os.makedirs(DATA_DIR, exist_ok=True)

# ----- Models -----
class Allocation(BaseModel):
    allocations: Dict[str, int]  # piece name -> skill points

class Move(BaseModel):
    from_x: int
    from_y: int
    to_x: int
    to_y: int
    promote: bool = False

class GameState(BaseModel):
    board: List[List[str]]
    turn: str
    allocations: Dict[str, int]

# ----- Helpers -----

def _game_path(game_id: str) -> str:
    return os.path.join(DATA_DIR, f"{game_id}.json")


def initial_board() -> List[List[str]]:
    """Return a standard shogi starting position using simple piece codes."""
    return [
        ["l", "n", "s", "g", "k", "g", "s", "n", "l"],
        ["", "r", "", "", "", "", "", "b", ""],
        ["p", "p", "p", "p", "p", "p", "p", "p", "p"],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["P", "P", "P", "P", "P", "P", "P", "P", "P"],
        ["", "B", "", "", "", "", "", "R", ""],
        ["L", "N", "S", "G", "K", "G", "S", "N", "L"],
    ]

# ----- Routes -----

@app.get('/games')
def list_games() -> List[str]:
    """Return list of existing game IDs."""
    return [f[:-5] for f in os.listdir(DATA_DIR) if f.endswith('.json')]


@app.post('/game')
def create_game(cfg: Allocation):
    """Create a new game with initial board and allocations."""
    game_id = str(uuid.uuid4())
    board = initial_board()
    state = GameState(board=board, turn='black', allocations=cfg.allocations)
    with open(_game_path(game_id), 'w') as f:
        json.dump(state.dict(), f)
    return {'game_id': game_id}


@app.get('/game/{game_id}')
def get_game(game_id: str) -> GameState:
    path = _game_path(game_id)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail='Game not found')
    with open(path) as f:
        data = json.load(f)
    return GameState(**data)


@app.post('/game/{game_id}/move')
def make_move(game_id: str, move: Move):
    path = _game_path(game_id)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail='Game not found')
    with open(path) as f:
        state = json.load(f)
    board = state['board']
    piece = board[move.from_y][move.from_x]
    if not piece:
        raise HTTPException(status_code=400, detail='No piece at from position')
    # simple bounds check
    if not (0 <= move.to_x < 9 and 0 <= move.to_y < 9):
        raise HTTPException(status_code=400, detail='Invalid move target')
    board[move.to_y][move.to_x] = piece
    board[move.from_y][move.from_x] = ''
    state['turn'] = 'white' if state['turn'] == 'black' else 'black'
    with open(path, 'w') as f:
        json.dump(state, f)
    return {'status': 'ok'}
