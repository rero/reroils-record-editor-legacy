import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { JsonSchemaFormModule, Bootstrap3FrameworkModule } from 'angular2-json-schema-form';
// import { JsonSchemaFormModule, Bootstrap3FrameworkModule, FrameworkLibraryService, WidgetLibraryService, Framework, JsonSchemaFormService } from 'angular2-json-schema-form';

import { AppComponent } from './app.component';


@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    Bootstrap3FrameworkModule,
    JsonSchemaFormModule.forRoot(Bootstrap3FrameworkModule)
 //    {
 //    	ngModule: JsonSchemaFormModule,
 //    	providers: [
 //    	    JsonSchemaFormService,
 //    	    FrameworkLibraryService,
 //    	    WidgetLibraryService,
 //    	    {provide: Framework, useClass: Bootstrap3FrameworkModule, multi: true}
 //    	]
	// }
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
