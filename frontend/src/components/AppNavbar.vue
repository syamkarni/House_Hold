<template>
  <nav>
    <ul>
      <li v-if="!authState.isAuthenticated">
        <router-link to="/login">Login</router-link>
      </li>
      <li v-if="!authState.isAuthenticated">
        <router-link to="/register">Register</router-link>
      </li>
      <li v-if="authState.isAuthenticated">
        <a href="#" @click.prevent="logoutUser">Logout</a>
      </li>
      <li v-if="authState.isAuthenticated && authState.userRole === 'admin'">
        <router-link to="/admin">Admin Dashboard</router-link>
      </li>
      <li v-if="authState.isAuthenticated && authState.userRole === 'customer'">
        <router-link to="/customer">Customer Dashboard</router-link>
      </li>
      <li v-if="authState.isAuthenticated && authState.userRole === 'customer'">
        <router-link to="/customer/profile">Profile</router-link>
      </li>
      <li v-if="authState.isAuthenticated && authState.userRole === 'professional'">
        <router-link to="/professional">Professional Dashboard</router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
import { authState, logout } from '@/services/auth';

export default {
  name: 'AppNavbar',
  setup() {
    const logoutUser = () => {
      logout();
      // removed localstoreage part
      window.location.href = '/login';
    };

    return {
      authState,
      logoutUser,
    };
  },
};
</script>