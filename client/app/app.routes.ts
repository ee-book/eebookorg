import { RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { UserRegisterComponent } from './user/user-register/user-register.component';
import { UserLoginComponent } from './user/user-login/user-login.component';
import { BookstoreComponent } from './bookstore/bookstore.component';


export const appRoutes = [
    {
        path: 'register',
        component: UserRegisterComponent
    },
    {
        path: 'login',
        component: UserLoginComponent
    },
    {
        path: 'bookstore',
        component: BookstoreComponent
    }
];
