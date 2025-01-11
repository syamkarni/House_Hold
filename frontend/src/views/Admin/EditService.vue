<template>
    <div>
      <h2>Edit Service</h2>
      <div v-if="error" style="color: red;">{{ error }}</div>
      <div v-if="service">
        <form @submit.prevent="updateService">
          <div>
            <label>Name:</label>
            <input type="text" v-model="service.name" required />
          </div>
          <div>
            <label>Avg Price:</label>
            <input type="number" v-model.number="service.price" required />
          </div>
          <div>
            <label>Avg Time Required (minutes):</label>
            <input type="number" v-model.number="service.time_required" required />
          </div>
          <div>
            <label>Description:</label>
            <textarea v-model="service.description" required></textarea>
          </div>
          <button type="submit">Update Service</button>
          <button type="button" @click="$router.back()">Cancel</button>
        </form>
      </div>
      <div v-else>
        <p>Loading service details...</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'EditService',
    data() {
      return {
        service: null,
        error: null,
      };
    },
    async created() {
      const serviceId = this.$route.params.id;
      try {
        // Fetch all services from admin endpoint and filter by ID
        const response = await axios.get('/admin/services', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        const services = response.data.services;
        this.service = services.find(s => s.id === parseInt(serviceId));
        if (!this.service) {
          this.error = 'Service not found';
        }
      } catch (err) {
        this.error = 'Error fetching service details.';
        console.error(err);
      }
    },
    methods: {
      async updateService() {
        try {
          await axios.put(
            `/admin/service/${this.service.id}`,
            this.service,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              },
            }
          );
          this.$router.push({ name: 'ManageServices' });
        } catch (error) {
          this.error = 'Error updating service.';
          console.error('Error updating service:', error);
        }
      },
    },
  };
  </script>
  