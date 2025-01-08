<template>
  <div>
    <h2>Request Service: {{ service?.name }}</h2>
    <div v-if="error" style="color: red;">{{ error }}</div>
    
    <div v-if="service">
      <p>{{ service.description }}</p>
      <div v-if="service.packages && service.packages.length">
        <h3>Available Packages:</h3>
        <ul>
          <li v-for="pkg in service.packages" :key="pkg.id">
            <h4>{{ pkg.name }}</h4>
            <p>{{ pkg.description }}</p>
            <p>Price: ${{ pkg.price }}</p>
            <p>Time Required: {{ pkg.time_required }} minutes</p>
            <button @click="submitRequest(pkg.id)">Request {{ pkg.name }}</button>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No packages available for this service.</p>
      </div>
    </div>
    <div v-else>
      <p>Loading service details...</p>
    </div>
  </div>
</template>

<script>
import axios from '@/plugins/axios';

export default {
  name: 'RequestService',
  data() {
    return {
      service: null,
      error: null,
    };
  },
  created() {
    const serviceId = this.$route.params.serviceId;
    this.fetchServiceDetails(serviceId);
  },
  methods: {
    async fetchServiceDetails(serviceId) {
      this.error = null;
      try {
        const response = await axios.get('/customer/services', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        const services = response.data.services;
        this.service = services.find((s) => s.id === parseInt(serviceId));
      } catch (error) {
        this.error = 'Error fetching service details.';
        console.error('Error fetching service details:', error);
      }
    },
    async submitRequest(packageId) {
      try {
        const payload = {
          service_id: this.service.id,
          package_id: packageId,
          remarks: ''  
        };
        await axios.post('/customer/service_request', payload, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        this.$router.push({ name: 'CustomerServiceRequests' });
      } catch (error) {
        this.error = 'Error submitting service request.';
        console.error('Error submitting service request:', error);
      }
    },
  },
};
</script>
