import { Component, ElementRef } from '@angular/core';

@Component({
  selector: 'rero-editor',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Editor';
  schema = {};
  form = {};
  model = {};
  displayData: any = null;

  constructor(elm: ElementRef){
    /** some process with your injected param **/
    this.schema = JSON.parse(elm.nativeElement.getAttribute('schema'));
    this.form = JSON.parse(elm.nativeElement.getAttribute('form'));
    this.model = JSON.parse(elm.nativeElement.getAttribute('model')); 
  }

  exampleOnSubmitFn(formData) {
    this.displayData = formData;
  }
}
