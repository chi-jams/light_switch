import { Component } from '@angular/core';
import { ColorPickerService } from 'ngx-color-picker';

@Component({
  selector: 'app-root',
  moduleId: 'src/app/app.component',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'app';

  constructor(private cpService: ColorPickerService) { }

  public onChange(color: string): string {
    const hsva = this.cpService.stringToHsva(color, true);
    console.log(hsva);
    return '';
  }
}
