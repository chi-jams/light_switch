import { Injectable } from '@angular/core';
import { Hsva } from 'ngx-color-picker';
import { LightSettings } from './lightSettings';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

const ws = webSocket('ws://localhost:8080/websocket');

@Injectable({
  providedIn: 'root'
})

export class WsService {
  constructor() {
    // Make an observer so that messages aren't stuck in a queue?
    ws.subscribe();
  }

  public sendColor(settings: LightSettings): void {
    console.log(settings);
    ws.next(settings);
  }
}
