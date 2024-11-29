<template>
    <form class="login-form" @submit.prevent="loginUser">
      <div class="form-group">
        <label>Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label>Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
      <div v-if="error" class="error">{{ error }}</div>
    </form>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  import { login } from '@/services/auth';
  
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
      async loginUser() {
        this.error = null;
        try {
          const response = await axios.post('/auth/login', {
            u_mail: this.email,
            password: this.password,
          });

        login(
            response.data.access_token,
            response.data.refresh_token,
            response.data.roles[0]
        );

        // removed localstorage method, all thanks to service/auth.js
        //   localStorage.setItem('access_token', response.data.access_token);
        //   localStorage.setItem('refresh_token', response.data.refresh_token);
        //   localStorage.setItem('user_role', response.data.roles[0]);

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

<style>
.login-form {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: white;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

input:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

button {
  width: 100%;
  padding: 0.75rem;
  background: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover {
  background: #357abd;
}

.error {
  color: #dc3545;
  margin-top: 1rem;
  font-size: 0.875rem;
}
</style>
  