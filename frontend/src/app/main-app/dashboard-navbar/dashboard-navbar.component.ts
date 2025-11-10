import { Component, inject } from '@angular/core';
import { MatToolbar } from '@angular/material/toolbar';
import { Router, RouterLink } from '@angular/router';
import { MatIconButton } from '@angular/material/button';
import { MatIcon } from '@angular/material/icon';
import { UserService } from '../../services/user-service';
import { MatMenu, MatMenuItem, MatMenuTrigger } from '@angular/material/menu';
import { CardComponent } from '../../utils/card-component/card-component';

@Component({
  selector: 'app-dashboard-navbar',
  imports: [
    MatToolbar,
    RouterLink,
    MatIconButton,
    MatIcon,
    MatMenuTrigger,
    MatMenu,
    MatMenuItem,
    CardComponent,
  ],
  templateUrl: './dashboard-navbar.component.html',
  styleUrl: './dashboard-navbar.component.css',
})
export class DashboardNavbar {
  private userService = inject(UserService);
  private router = inject(Router);

  constructor() {
    if (!this.userService.isLoggedIn()) {
      this.router.navigate(['login']).then(() => {});
    }
  }

  logout() {
    this.userService.logOut();
    this.router.navigate(['login']).then(() => {});
  }
}
