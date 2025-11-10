import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptorInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    req.headers.append('Authorization', 'Bearer ' + token);
  }
  return next(req);
};
