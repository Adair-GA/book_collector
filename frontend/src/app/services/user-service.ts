import { inject, Injectable, signal, WritableSignal } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { catchError, map, Observable, of, switchMap } from 'rxjs';
import { jwtDecode } from 'jwt-decode';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private apiUrl = environment.API_URL;
  private client = inject(HttpClient);

  isLoggedIn: WritableSignal<boolean>;

  constructor() {
    const token = localStorage.getItem('authToken');
    if (!token) {
      this.isLoggedIn = signal(false);
      return;
    }

    const decrypted = jwtDecode(token);
    if (decrypted.exp != null && decrypted.exp > Date.now() / 1000) {
      console.log(decrypted);
      this.isLoggedIn = signal(true);
    } else {
      this.isLoggedIn = signal(false);
    }
  }

  login(email: string, password: string): Observable<{ success: boolean }> {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    return this.client.post<{ access_token: string }>(`${this.apiUrl}/auth/login`, formData).pipe(
      map((value: { access_token: string }) => {
        localStorage.setItem('authToken', value.access_token);
        this.isLoggedIn.set(true);
        return { success: true };
      }),
      catchError((err) => {
        if (err instanceof HttpErrorResponse && err.status == 401) {
          return of({ success: false });
        }
        throw err;
      }),
    );
  }

  register(email: string, password: string): Observable<{ success: boolean }> {
    return this.client
      .post(`${this.apiUrl}/auth/register`, {
        email,
        password,
      })
      .pipe(
        switchMap((_) => {
          return this.login(email, password);
        }),
        catchError((err) => {
          if (err instanceof HttpErrorResponse && err.status == 401) {
            return of({ success: false });
          }
          throw err;
        }),
      );
  }

  logOut() {
    localStorage.removeItem('authToken');
    this.isLoggedIn.set(false);
  }
}
