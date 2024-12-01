import { reactive } from 'vue';

export const authState = reactive({
  isAuthenticated: !!localStorage.getItem('access_token'),
  userRole: localStorage.getItem('user_role') || null,
  profileComplete: false, 
});

export function login(accessToken, refreshToken, userRole) {
  localStorage.setItem('access_token', accessToken);
  localStorage.setItem('refresh_token', refreshToken);
  localStorage.setItem('user_role', userRole);
  authState.isAuthenticated = true;
  authState.userRole = userRole;

  const tokenPayload = JSON.parse(atob(accessToken.split('.')[1]));
  const identity = tokenPayload.sub || tokenPayload.identity;
  authState.profileComplete = identity.profile_complete || false;
}

export function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user_role');
  authState.isAuthenticated = false;
  authState.userRole = null;
  authState.profileComplete = false; 
}
