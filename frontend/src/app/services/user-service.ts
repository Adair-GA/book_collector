import { inject, Inject, Injectable, signal } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { catchError, map, Observable, of, tap } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private apiUrl = environment.API_URL;
  private client = inject(HttpClient)

  isLoggedIn = signal(localStorage.getItem("authToken") !== null)

  login(email: string, password: string): Observable<{ success: boolean }> {
    let formData = new FormData()
    formData.append("username", email)
    formData.append("password", password)

    return this.client.post(`${this.apiUrl}/auth/login`, formData).pipe(
      map((value: any) => {
        localStorage.setItem("authToken", value.access_token);

        return { success: true }
      }),
      catchError(err => {
        if (err instanceof HttpErrorResponse && err.status == 401) {
          return of({ success: false })
        }
        throw err
      })
    )
  }

}
