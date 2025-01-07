<template>
    <div>
      <h2>Your Service Requests</h2>
      <div v-if="error" style="color: red;">{{ error }}</div>
      <table v-if="requests.length > 0">
        <thead>
          <tr>
            <th>Service</th>
            <th>Professional</th>
            <th>Date of Request</th>
            <th>Status</th>
            <th>Remarks</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in requests" :key="request.id">
            <td>{{ request.service.name }}</td>
            <td>
              <div v-if="request.professional">
                <!-- {{ request.professional.name }} ({{ request.professional.service_type }}) -->
                {{ request.professional.name }} ({{ request.professional.service_name }}) <!-- temporary fix(dosen't work though, need to replace it by serivce_id) -->
              </div>
              <div v-else>
                Not Assigned
              </div>
            </td>
            <td>{{ request.date_of_request }}</td>
            <td>{{ request.service_status }}</td>
            <td>{{ request.remarks }}</td>
            <td>
              <button
                v-if="['requested', 'assigned'].includes(request.service_status)"
                @click="cancelRequest(request.id)"
              >
                Cancel
              </button>
              <button
                v-if="request.service_status === 'completed' && !request.reviewed"
                @click="provideReview(request.id)"
              >
                Review
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else>
        <p>You have no service requests.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'CustomerServiceRequests',
    data() {
      return {
        requests: [],
        error: null,
      };
    },
    created() {
      this.fetchServiceRequests();
    },
    methods: {
      async fetchServiceRequests() {
        this.error = null;
        try {
          const response = await axios.get('/customer/service_requests', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          });
          this.requests = response.data.requests;
        } catch (error) {
          this.error = 'Error fetching service requests.';
          console.error('Error fetching service requests:', error);
        }
      },
      async cancelRequest(requestId) {
        try {
          await axios.put(
            `/customer/service_requests/${requestId}/cancel`,
            {},
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              },
            }
          );
          this.fetchServiceRequests();
        } catch (error) {
          console.error('Error cancelling service request:', error);
        }
      },
      provideReview(requestId) {
        this.$router.push({ name: 'ProvideReview', params: { requestId } });
      },
    },
  };
  </script>
  