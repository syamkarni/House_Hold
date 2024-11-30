<template>
    <div>
      <h2>Available Services</h2>
      <div v-if="error" style="color: red;">{{ error }}</div>
      <div v-if="services.length > 0">
        <ul>
          <li v-for="service in services" :key="service.id">
            <h3>{{ service.name }}</h3>
            <p>{{ service.description }}</p>
            <p>Price: ${{ service.price }}</p>
            <p>Time Required: {{ service.time_required }} minutes</p>
            <button @click="requestService(service.id)">Request Service</button>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No services available at the moment.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'AvailableServices',
    data() {
      return {
        services: [],
        error: null,
      };
    },
    created() {
      this.fetchServices();
    },
    methods: {
      async fetchServices() {
        this.error = null;
        try {
          const response = await axios.get('/customer/services', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          });
          this.services = response.data.services;
        } catch (error) {
          this.error = 'Error fetching services.';
          console.error('Error fetching services:', error);
        }
      },
      requestService(serviceId) {
        this.$router.push({ name: 'RequestService', params: { serviceId } });
      },
    },
  };
  </script>
  