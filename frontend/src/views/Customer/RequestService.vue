<template>
    <div>
      <h2>Request Service</h2>
      <div v-if="error" style="color: red;">{{ error }}</div>
      <div v-if="service">
        <h3>{{ service.name }}</h3>
        <p>{{ service.description }}</p>
        <form @submit.prevent="submitRequest">
          <div>
            <label for="remarks">Remarks:</label>
            <textarea id="remarks" v-model="remarks"></textarea>
          </div>
          <button type="submit">Submit Request</button>
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
    name: 'RequestService',
    data() {
      return {
        service: null,
        remarks: '',
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
      async submitRequest() {
        try {
          await axios.post(
            '/customer/service_requests',
            {
              service_id: this.service.id,
              remarks: this.remarks,
            },
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              },
            }
          );
          this.$router.push({ name: 'CustomerServiceRequests' });
        } catch (error) {
          this.error = 'Error submitting service request.';
          console.error('Error submitting service request:', error);
        }
      },
    },
  };
  </script>
  