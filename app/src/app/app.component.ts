import { Component } from '@angular/core';
import { ColorPickerService } from 'ngx-color-picker';
import { WsService } from './ws.service';

@Component({
  selector: 'app-root',
  moduleId: 'src/app/app.component',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'app';

  constructor(private cpService: ColorPickerService, private wsService: WsService) { }

  public onChange(color: string): void {
    const hsva = this.cpService.stringToHsva(color, true);
    console.log(hsva);
    this.wsService.sendColor(hsva);
  }
}
