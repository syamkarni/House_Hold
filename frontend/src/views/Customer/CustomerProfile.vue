<template>
    <div>
      <h2>Complete Your Profile</h2>
      <form @submit.prevent="updateProfile">
        <div>
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="name" required />
        </div>
        <div>
          <label for="phone">Phone:</label>
          <input type="text" id="phone" v-model="phone" required />
        </div>
        <div>
          <label for="address">Address:</label>
          <input type="text" id="address" v-model="address" required />
        </div>
        <button type="submit">Save Profile</button>
      </form>
      <p v-if="message" :class="{ success: success, error: !success }">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  import { authState } from '@/services/auth';
  
  export default {
    name: 'CustomerProfile',
    data() {
      return {
        name: '',
        phone: '',
        address: '',
        message: '',
        success: false,
      };
    },
    created() {
      this.fetchProfile();
    },
    methods: {
      async fetchProfile() {
        try {
          const response = await axios.get('/customer/profile', {
            headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
          });
          const profile = response.data.profile;
          this.name = profile.name || '';
          this.phone = profile.phone || '';
          this.address = profile.address || '';
        } catch (error) {
          console.error('Error fetching profile:', error);
        }
      },
      async updateProfile() {
        try {
          await axios.put(
            '/customer/profile',
            {
              name: this.name,
              phone: this.phone,
              address: this.address,
            },
            {
              headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
            }
          );
          this.message = 'Profile updated successfully.';
          this.success = true;
  

          authState.profileComplete = true;
          localStorage.setItem('profile_complete', 'true');
  
          this.$router.push('/customer');
        } catch (error) {
          console.error('Error updating profile:', error);
          this.message = 'Failed to update profile.';
          this.success = false;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .success {
    color: green;
  }
  .error {
    color: red;
  }
  </style>
  