import { ComponentsModule } from './shared/components/components.module';
import { SharedModule } from './shared/shared.module';
import { JobModule } from './job/job.module';
import { GithubService } from './searching/search.service';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgxPaginationModule } from 'ngx-pagination';

import { GrowlModule } from 'primeng/components/growl/growl';
// import { ConfirmDialogModule } from 'primeng/primeng';

import { AppComponent } from './app.component';
import { UserComponent } from './user/user.component';
import { UserRegisterComponent } from './user/user-register/user-register.component';
import { UserLoginComponent } from './user/user-login/user-login.component';
import { FormControlComponent } from './common/dynamic-form/form-control.component';
import { appRoutes } from './app.routes';
import { CommonModule } from './common/common.module';
import { AuthService, AuthGuard } from './common/auth.service';
import { HttpService, SimpleRequest } from './common/http.service';
import { JobService } from './job/job.service';
import { BookstoreComponent } from './bookstore/bookstore.component';
import { SettingsComponent } from './settings/settings.component';
import { JobComponent } from './job/job.component';
import { JobHistoryDetailComponent } from './job/history/job-history-detail/job-history-detail.component';
import { JobHistoryListComponent } from './job/history/job-history-list/job-history-list.component';
import { JobConfigCreateComponent } from './job/config/job-config-create/job-config-create.component';
import { JobConfigListComponent } from './job/config/job-config-list/job-config-list.component';
import { SearchingComponent } from './searching/searching.component';
import { SearchFormComponent } from './searching/search-form/search-form.component';
import { SearchResultComponent } from './searching/search-result/search-result.component';
import { JobConfigDetailComponent } from './job/config/job-config-detail/job-config-detail.component';
import { MaterialModule } from '@angular/material';
import { ConfirmBoxComponent } from './shared/components/confirm-box/confirm-box.component';
import { SchemaFormModule, WidgetRegistry, DefaultWidgetRegistry } from 'angular2-schema-form';


@NgModule({
  declarations: [
    AppComponent,
    UserComponent,
    UserRegisterComponent,
    FormControlComponent,
    UserLoginComponent,
    BookstoreComponent,
    SettingsComponent,
    JobComponent,
    JobHistoryDetailComponent,
    JobHistoryListComponent,
    JobConfigCreateComponent,
    JobConfigListComponent,
    JobConfigDetailComponent,
    SearchingComponent,
    SearchFormComponent,
    SearchResultComponent,
    // ConfirmBoxComponent,
  ],
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    FormsModule,
    CommonModule,
    BrowserAnimationsModule,
    NgxPaginationModule,
    // RouterModule,
    GrowlModule,
    // JobModule,
    MaterialModule,
    SharedModule,
    ComponentsModule,
    SchemaFormModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [
    AuthService,
    HttpService,
    JobService,
    GithubService,
    SimpleRequest,
    AuthGuard,
    {provide: WidgetRegistry, useClass: DefaultWidgetRegistry},
  ],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }
