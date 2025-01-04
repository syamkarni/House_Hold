<template>
  <div>
    <h2>Complete Your Professional Profile</h2>
    <form @submit.prevent="updateProfile">
      <div>
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="name" required />
      </div>
      <div>
        <label for="service_id">Service:</label>
        <select id="service_id" v-model="service_id" required>
          <option disabled value="">Please select a service</option>
          <option v-for="service in services" :key="service.id" :value="service.id">
            {{ service.name }}
          </option>
        </select>
      </div>
      <div>
        <label for="experience">Experience (years):</label>
        <input type="number" id="experience" v-model="experience" min="0" required />
      </div>
      <div>
        <label for="description">Description:</label>
        <textarea id="description" v-model="description" required></textarea>
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
  name: 'ProfessionalProfile',
  data() {
    return {
      name: '',
      service_id: '',  
      experience: '',
      description: '',
      services: [], 
      message: '',
      success: false,
    };
  },
  created() {
    this.fetchProfile();
    this.fetchServices(); 
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await axios.get('/professional/profile', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        });
        const profile = response.data.profile;
        this.name = profile.name || '';
        this.service_id = profile.service_id || ''; 
        this.experience = profile.experience || '';
        this.description = profile.description || '';
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
    async fetchServices() {
      try {
        const response = await axios.get('/professional/services', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        });
        this.services = response.data.services;
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    },
    async updateProfile() {
      try {
        await axios.put(
          '/professional/profile',
          {
            name: this.name,
            service_id: this.service_id,  
            experience: this.experience,
            description: this.description,
          },
          {
            headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
          }
        );
        this.message = 'Profile updated successfully. Awaiting admin approval.';
        this.success = true;

        authState.profileComplete = true;
        localStorage.setItem('profile_complete', 'true');

        this.$router.push('/professional');
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
