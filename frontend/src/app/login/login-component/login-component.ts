import { Component, inject, signal } from '@angular/core';
import { UserService } from '../../services/user-service';
import { MatCard, MatCardContent, MatCardHeader } from '@angular/material/card';
import { MatFormField } from '@angular/material/form-field';
import { MatInput } from '@angular/material/input';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatAnchor, MatButton } from '@angular/material/button';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login-component',
  imports: [
    MatCard,
    MatCardHeader,
    MatCardContent,
    MatFormField,
    MatInput,
    ReactiveFormsModule,
    MatAnchor,
    MatButton,
  ],
  templateUrl: './login-component.html',
  styleUrl: './login-component.css',
})
export class LoginComponent {
  userService = inject(UserService);
  protected router = inject(Router);
  mode = signal<'login' | 'register'>('login');
  form: FormGroup;

  public constructor(formBuilder: FormBuilder) {
    this.form = formBuilder.group({
      email: new FormControl('', [Validators.email, Validators.required]),
      password: new FormControl('', [Validators.required]),
    });
  }

  submit() {
    if (!this.form.valid) {
      return;
    }
    let result;
    if (this.mode() === 'register') {
      result = this.registerSubmit();
    } else {
      result = this.loginSubmit();
    }

    result.subscribe((res) => {
      if (res.success) {
        this.router.navigate(['/']).then();
      } else {
        alert('Error');
      }
    });
  }

  private loginSubmit() {
    return this.userService.login(this.form.get('email')?.value, this.form.get('password')?.value);
  }

  private registerSubmit() {
    return this.userService.register(
      this.form.get('email')?.value,
      this.form.get('password')?.value,
    );
  }

  changeMode() {
    this.mode.update((current) => {
      if (current == 'login') {
        return 'register';
      } else {
        return 'login';
      }
    });
  }
}
