<template>
  <div>
    <h2>Complete Your Professional Profile</h2>
    <form @submit.prevent="updateProfile">
      <div>
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="name" required />
      </div>
      <div>
        <label for="service_type">Service Type:</label>
        <input type="text" id="service_type" v-model="service_type" required />
      </div>
      <div>
        <label for="experience">Experience (years):</label>
        <input type="number" id="experience" v-model="experience" required />
      </div>
      <div>
        <label for="description">Description:</label>
        <textarea id="description" v-model="description" required></textarea>
      </div>
      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Saving...' : 'Save Profile' }}
      </button>
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
      service_type: '',
      experience: '',
      description: '',
      message: '',
      success: false,
      isLoading: false, // New loading state
    };
  },
  created() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await axios.get('/professional/profile', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        });
        const profile = response.data.profile;
        this.name = profile.name || '';
        this.service_type = profile.service_type || '';
        this.experience = profile.experience || '';
        this.description = profile.description || '';
      } catch (error) {
        console.error('Error fetching profile:', error);
        this.message = 'Failed to load profile data. Please try again later.';
        this.success = false;
      }
    },
    async updateProfile() {
      if (!this.validateFields()) return;

      this.isLoading = true; 
      try {
        await axios.put(
          '/professional/profile',
          {
            name: this.name,
            service_type: this.service_type,
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
        const errorMessage =
          error.response?.data?.message || 'Failed to update profile. Please try again.';
        this.message = errorMessage;
        this.success = false;
      } finally {
        this.isLoading = false; 
      }
    },
    validateFields() {
      if (!this.name || !this.service_type || this.experience <= 0 || !this.description) {
        this.message = 'Please fill out all fields correctly.';
        this.success = false;
        return false;
      }
      return true;
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
button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
