import { Routes } from '@angular/router';
import { App } from './app';
import { LoginComponent } from './login/login-component/login-component';

export const routes: Routes = [
    {
        path: "",
        component: App,
        children: [
            {
                path: "login",
                component: LoginComponent
            }
        ]
    }
];
