<template>
    <div>
      <h2>Assigned Service Requests</h2>
      <div v-if="error" style="color: red;">{{ error }}</div>
      <table v-if="requests.length > 0">
        <thead>
          <tr>
            <th>Service</th>
            <th>Date of Request</th>
            <th>Status</th>
            <th>Customer Remarks</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in requests" :key="request.id">
            <td>{{ request.service.name }}</td>
            <td>{{ request.date_of_request }}</td>
            <td>{{ request.service_status }}</td>
            <td>{{ request.remarks }}</td>
            <td>
              <button
                v-if="request.service_status === 'assigned'"
                @click="acceptRequest(request.id)"
              >
                Accept
              </button>
              <button
                v-if="request.service_status === 'assigned'"
                @click="rejectRequest(request.id)"
              >
                Reject
              </button>
              <button
                v-if="request.service_status === 'accepted'"
                @click="completeRequest(request.id)"
              >
                Mark as Completed
              </button>

            </td>
          </tr>
        </tbody>
      </table>
      <div v-else>
        <p>No assigned service requests at the moment.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'AssignedRequests',
    data() {
      return {
        requests: [],
        error: null,
      };
    },
    created() {
      this.fetchAssignedRequests();
    },
    methods: {
      async fetchAssignedRequests() {
        this.error = null;
        try {
          const response = await axios.get('/professional/service_requests', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          });
          this.requests = response.data.requests;
        } catch (error) {
          this.error = 'Error fetching assigned requests.';
          console.error('Error fetching assigned requests:', error);
        }
      },
      async acceptRequest(requestId) {
        try {
          await axios.put(
            `/professional/service_request/${requestId}/accept`,
            {},
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              },
            }
          );
          this.fetchAssignedRequests();
        } catch (error) {
          console.error('Error accepting request:', error);
        }
      },
      async rejectRequest(requestId) {
        try {
          await axios.put(
            `/professional/service_request/${requestId}/reject`,
            {},
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              },
            }
          );
          this.fetchAssignedRequests();
        } catch (error) {
          console.error('Error rejecting request:', error);
        }
      },
      async completeRequest(requestId) {
        try {
          await axios.put(
            `/professional/service_request/${requestId}/complete`,
            {},
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              },
            }
          );
          this.fetchAssignedRequests();
        } catch (error) {
          console.error('Error marking request as completed:', error);
        }
      },
    },
  };
  </script>
  