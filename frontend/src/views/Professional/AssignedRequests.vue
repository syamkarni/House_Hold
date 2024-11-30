<template>
  <div>
    <h2>Unassigned Service Requests</h2>
    <div v-if="error" style="color: red;">{{ error }}</div>
    <table v-if="unassignedRequests.length > 0">
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
        <tr v-for="request in unassignedRequests" :key="request.id">
          <td>{{ request.service.name }}</td>
          <td>{{ request.date_of_request }}</td>
          <td>{{ request.service_status }}</td>
          <td>{{ request.remarks }}</td>
          <td>
            <button @click="acceptRequest(request.id)">Accept</button>
            <button @click="rejectRequest(request.id)">Reject</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else>
      <p>No unassigned service requests at the moment.</p>
    </div>

    <h2>Assigned Service Requests</h2>
    <table v-if="assignedRequests.length > 0">
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
        <tr v-for="request in assignedRequests" :key="request.id">
          <td>{{ request.service.name }}</td>
          <td>{{ request.date_of_request }}</td>
          <td>{{ request.service_status }}</td>
          <td>{{ request.remarks }}</td>
          <td>
            <button @click="completeRequest(request.id)">Mark as Completed</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else>
      <p>No assigned service requests at the moment.</p>
    </div>

    <h2>Service Request History</h2>
    <div v-if="historyError" style="color: red;">{{ historyError }}</div>
    <table v-if="historyRequests.length > 0">
      <thead>
        <tr>
          <th>Service</th>
          <th>Date of Request</th>
          <th>Date of Completion</th>
          <th>Status</th>
          <th>Customer Remarks</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in historyRequests" :key="request.id">
          <td>{{ request.service.name }}</td>
          <td>{{ request.date_of_request }}</td>
          <td>{{ request.date_of_completion || 'N/A' }}</td>
          <td>{{ request.service_status }}</td>
          <td>{{ request.remarks }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else>
      <p>No historical service requests at the moment.</p>
    </div>
  </div>
</template>

<script>
import axios from '@/plugins/axios';

export default {
  name: 'AssignedRequests',
  data() {
    return {
      unassignedRequests: [],
      assignedRequests: [],
      historyRequests: [],
      error: null,
      historyError: null,
    };
  },
  created() {
    this.fetchUnassignedRequests();
    this.fetchAssignedRequests();
    this.fetchServiceRequestHistory();
  },
  methods: {
    async fetchUnassignedRequests() {
      this.error = null;
      try {
        const response = await axios.get('/professional/unassigned_service_requests', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        this.unassignedRequests = response.data.requests;
      } catch (error) {
        this.error = 'Error fetching unassigned requests.';
        console.error('Error fetching unassigned requests:', error);
      }
    },
    async fetchAssignedRequests() {
      this.error = null;
      try {
        const response = await axios.get('/professional/service_requests', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        this.assignedRequests = response.data.requests;
      } catch (error) {
        this.error = 'Error fetching assigned requests.';
        console.error('Error fetching assigned requests:', error);
      }
    },
    async fetchServiceRequestHistory() {
      this.historyError = null;
      try {
        const response = await axios.get('/professional/service_request_history', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        this.historyRequests = response.data.requests;
      } catch (error) {
        this.historyError = 'Error fetching service request history.';
        console.error('Error fetching service request history:', error);
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
        this.fetchUnassignedRequests();
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
        this.fetchUnassignedRequests();
        this.fetchAssignedRequests();
        this.fetchServiceRequestHistory();
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
        this.fetchServiceRequestHistory();
      } catch (error) {
        console.error('Error marking request as completed:', error);
      }
    },
  },
};
</script>
