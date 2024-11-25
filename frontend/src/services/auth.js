import { reactive } from 'vue';

export const authState = reactive({
  isAuthenticated: !!localStorage.getItem('access_token'),
  userRole: localStorage.getItem('user_role') || null,
});

export function login(accessToken, refreshToken, userRole) {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
    localStorage.setItem('user_role', userRole);
    authState.isAuthenticated = true;
    authState.userRole = userRole;
  }

export function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user_role');
  authState.isAuthenticated = false;
  authState.userRole = null;
}
