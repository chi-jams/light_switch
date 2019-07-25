import { Injectable } from '@angular/core';
import { Hsva } from 'ngx-color-picker';
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

  public sendColor(color: Hsva): void {
    const lightSettings = {
      hue: Math.round(65535 * color.h),
      sat: Math.round(255 * color.s),
      bri: Math.round(255 * color.v),
      on: color.v > 0
    };
    ws.next(lightSettings);
  }
}
