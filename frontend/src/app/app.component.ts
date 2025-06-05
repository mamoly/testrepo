import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  template: `
    <h1>Shogi App</h1>
    <button (click)="createGame()">Start Game</button>
    <pre>{{ gameId }}</pre>
  `
})
export class AppComponent {
  gameId?: string;
  constructor(private http: HttpClient) {}
  createGame() {
    const alloc = { allocations: { pawn: 50 } };
    const url = 'http://localhost:8000/game';
    this.http.post<any>(url, alloc).subscribe(res => this.gameId = res.game_id);
    this.http.post<any>('/game', alloc).subscribe(res => this.gameId = res.game_id);
  }
}
