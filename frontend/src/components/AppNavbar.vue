<template>
  <nav>
    <ul>
      <li v-if="!isAuthenticated">
        <router-link to="/login">Login</router-link>
      </li>
      <li v-if="!isAuthenticated">
        <router-link to="/register">Register</router-link>
      </li>
      <li v-if="isAuthenticated">
        <a href="#" @click.prevent="logout">Logout</a>
      </li>
      <li v-if="isAuthenticated && userRole === 'admin'">
        <router-link to="/admin">Admin Dashboard</router-link>
      </li>
      <li v-if="isAuthenticated && userRole === 'customer'">
        <router-link to="/customer">Customer Dashboard</router-link>
      </li>
      <li v-if="isAuthenticated && userRole === 'professional'">
        <router-link to="/professional">Professional Dashboard</router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'AppNavbar', 
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('access_token');
    },
    userRole() {
      return localStorage.getItem('user_role');
    },
  },
  methods: {
    logout() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user_role');
      this.$router.push('/login');
    },
  },
};
</script>
