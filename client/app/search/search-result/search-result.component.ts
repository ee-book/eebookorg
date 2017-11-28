import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Search } from '../models/search-model';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.scss']
})
export class SearchResultComponent implements OnInit {
  items: Object[] = [
    {
      'item_id': '1',
      'name': 'Suzy Cuningham',
      'description': 'updated her account',
      'icon': 'account_circle',
      'created' : '07/13/2016 11:05 AM'
    }, {
      'item_id': '2',
      'name': 'Bobby Daniels',
      'description': 'made a deposit of $25.15',
      'icon': 'account_balance_wallet',
      'created' : '07/01/2016 03:41 PM'
    }, {
      'item_id': '3',
      'name': 'John Walker',
      'description': 'changed refresh settings on their account',
      'icon': 'autorenew',
      'created' : '06/15/2016 09:02 AM'
    }, {
      'item_id': '4',
      'name': 'Eddy Stevens',
      'description': 'liked the latest announcements',
      'icon': 'thumb_up',
      'created' : '03/23/2016 11:01 PM'
    }, {
      'item_id': '5',
      'name': 'Jan Williams',
      'description': 'sent a personal message to a user',
      'icon': 'message',
      'created' : '12/23/2015 11:05 AM'
    }
  ];
  @Input() searchModel: Search;

  constructor() { }

  ngOnInit() {
  }

}
