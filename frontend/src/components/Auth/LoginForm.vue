<template>
    <form @submit.prevent="login">
      <div>
        <label>Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
      <div v-if="error" style="color: red;">{{ error }}</div>
    </form>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'LoginForm',
    data() {
      return {
        email: '',
        password: '',
        error: null,
      };
    },
    methods: {
      async login() {
        this.error = null;
        try {
          const response = await axios.post('/auth/login', {
            u_mail: this.email,
            password: this.password,
          });
          localStorage.setItem('access_token', response.data.access_token);
          localStorage.setItem('refresh_token', response.data.refresh_token);
          localStorage.setItem('user_role', response.data.roles[0]);

          const role = response.data.roles[0];
          if (role === 'admin') {
            this.$router.push('/admin');
          } else if (role === 'customer') {
            this.$router.push('/customer');
          } else if (role === 'professional') {
            this.$router.push('/professional');
          }
        } catch (err) {
            //remove this, no debugging required anymore in the future, do not remove by undo!!!:
          this.error = ("Login failed. Please check your credentials.", err.response?.data || err.message);
        }
      },
    },
  };
  </script>
  