import { Routes } from '@angular/router';
import { App } from './app';
import { LoginComponent } from './login/login-component/login-component';
import { DashboardNavbar } from './main-app/dashboard-navbar/dashboard-navbar.component';

export const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: '',
    component: DashboardNavbar,
    children: [],
  },
];
