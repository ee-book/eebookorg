import { Router } from '@angular/router';
import { Component, OnInit, AfterContentChecked, OnChanges, AfterViewChecked, AfterContentInit } from '@angular/core';

@Component({
  selector: 'app-job',
  templateUrl: './job.component.html',
  styleUrls: ['./job.component.scss']
})
export class JobComponent implements OnInit, AfterViewChecked {
  navMenu: Object[] = [{
    title: 'Config',
    route: '/job/config/list',
    icon: 'perm_data_setting',
  }, {
    title: 'History',
    route: '/job/history/list',
    icon: 'change_history',
  }];

  currentComponent = '';

  constructor(
    private router: Router
  ) { }

  ngOnInit() {
    this.currentComponent = this.router.url.split('/')[2];
  }

  ngAfterViewChecked() {
    this.currentComponent = this.router.url.split('/')[2];
  }

}
