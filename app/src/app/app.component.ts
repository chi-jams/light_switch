import { Component } from '@angular/core';
import { MatSlideToggleChange } from '@angular/material';
import { ColorPickerService } from 'ngx-color-picker';
import { LightSettings } from './lightSettings';
import { WsService } from './ws.service';

@Component({
  selector: 'app-root',
  moduleId: 'src/app/app.component',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'app';
  on = true;
  light = new LightSettings();

  constructor(private cpService: ColorPickerService, private wsService: WsService) { }

  public onColorChange(color: string, on: boolean): void {
    const hsva = this.cpService.stringToHsva(color, true);
    this.light.hue = Math.round(65535 * hsva.h);
    this.light.sat = Math.round(255 * hsva.s);
    this.light.bri = Math.round(255 * hsva.v);
    this.light.on = this.on && hsva.v > 0;
    this.wsService.sendColor(this.light);
  }

  public onSwitchChange(toggle: MatSlideToggleChange) {
    console.log(toggle.checked);
    this.on = toggle.checked;
    this.light.on = this.on && this.light.bri > 0;
    this.wsService.sendColor(this.light);
  }
}
