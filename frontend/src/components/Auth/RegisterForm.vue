<template>
    <form @submit.prevent="register">
      <div>
        <label>Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <div>
        <label>Role:</label>
        <select v-model="role" required>
          <option disabled value="">Please select one</option>
          <option value="customer">Customer</option>
          <option value="professional">Professional</option>
        </select>
      </div>
      <button type="submit">Register</button>
      <div v-if="error" style="color: red;">{{ error }}</div>
    </form>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'RegisterForm',
    data() {
      return {
        email: '',
        password: '',
        role: '',
        error: null,
      };
    },
    methods: {
      async register() {
        this.error = null;
        try {
          await axios.post('/auth/register', {
            u_mail: this.email,
            password: this.password,
            role: this.role,
          });
          this.$router.push('/login');
        } catch (err) {
          this.error = 'Registration failed. Please try again.';
        }
      },
    },
  };
  </script>
  