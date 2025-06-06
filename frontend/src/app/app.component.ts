import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface GameState {
  board: string[][];
  turn: string;
  allocations: {[key: string]: number};
}

@Component({
  selector: 'app-root',
  template: `
    <h1>Shogi App</h1>
    <button (click)="createGame()">Start Game</button>
    <div *ngIf="gameId">
      <p>Game ID: {{ gameId }}</p>
      <table class="board">
        <tr *ngFor="let row of board; let y = index">
          <td *ngFor="let cell of row; let x = index" (click)="select(x, y)">
            {{ cell || '.' }}
          </td>
        </tr>
      </table>
      <p>Selected: {{ selX }},{{ selY }}</p>
      <button (click)="move(xField.value, yField.value)" *ngIf="selX !== null" >Move to
        <input #xField type="number" min="0" max="8" placeholder="x">
        <input #yField type="number" min="0" max="8" placeholder="y">
      </button>
    </div>
  `,
  styles: [
    `.board td { width:20px; height:20px; text-align:center; border:1px solid #ccc; }`
  ]
})
export class AppComponent {
  gameId?: string;
  board: string[][] = [];
  selX: number | null = null;
  selY: number | null = null;
  constructor(private http: HttpClient) {}

  createGame() {
    const alloc = { allocations: { pawn: 50 } };
    const url = 'http://localhost:8000/game';
    this.http.post<any>(url, alloc).subscribe(res => {
      this.gameId = res.game_id;
      this.loadGame();
    });
  }

  loadGame() {
    if (!this.gameId) return;
    this.http.get<GameState>(`http://localhost:8000/game/${this.gameId}`)
      .subscribe(state => this.board = state.board);
  }

  select(x: number, y: number) {
    this.selX = x;
    this.selY = y;
  }

  move(x: string, y: string) {
    if (this.selX === null || this.selY === null || !this.gameId) return;
    const to_x = parseInt(x, 10);
    const to_y = parseInt(y, 10);
    const url = `http://localhost:8000/game/${this.gameId}/move`;
    this.http.post(url, { from_x: this.selX, from_y: this.selY, to_x, to_y })
      .subscribe(() => {
        this.selX = this.selY = null;
        this.loadGame();
      });
    this.http.post<any>('/game', alloc).subscribe(res => this.gameId = res.game_id);
  }
}
