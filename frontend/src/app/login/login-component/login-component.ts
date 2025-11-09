import { Component, inject, signal } from '@angular/core';
import { UserService } from '../../services/user-service';
import { MatCard, MatCardHeader, MatCardContent, MatCardActions } from '@angular/material/card'
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule, MatInput } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormBuilder, FormControl, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule, MatAnchor } from '@angular/material/button';

@Component({
  selector: 'app-login-component',
  imports: [MatCard, MatCardHeader, MatCardContent, MatFormField, MatInput, ReactiveFormsModule, MatLabel, MatCardActions, MatAnchor],
  templateUrl: './login-component.html',
  styleUrl: './login-component.css',
})
export class LoginComponent {
  private userService = inject(UserService);
  mode = signal<'login' | 'register'>('login')
  form: FormGroup;


  public constructor(formBuilder: FormBuilder) {
    this.form = formBuilder.group({
      email: new FormControl('', [Validators.email, Validators.required]),
      password: new FormControl('', [Validators.required])
    })
  }


  loginSubmit() {
    if (!this.form.valid) {
      return
    }
    this.userService.login(this.form.get("email")?.value, this.form.get("password")?.value).subscribe(v => console.log(v))
  }

  registerSubmit() {
    if (!this.form.valid) {
      return
    }
    this.userService.login(this.form.get("email")?.value, this.form.get("password")?.value).subscribe(v => console.log(v))
  }

}
