from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import uuid
import json
import os

app = FastAPI()
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

# ----- Routes -----
@app.post('/game')
def create_game(cfg: Allocation):
    """Create a new game with initial board and allocations."""
    game_id = str(uuid.uuid4())
    # simplified initial board: 9x9 empty board
    board = [['' for _ in range(9)] for _ in range(9)]
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
    # This is just a placeholder; actual shogi logic is omitted
    board = state['board']
    board[move.to_y][move.to_x] = board[move.from_y][move.from_x]
    board[move.from_y][move.from_x] = ''
    state['turn'] = 'white' if state['turn'] == 'black' else 'black'
    with open(path, 'w') as f:
        json.dump(state, f)
    return {'status': 'ok'}
