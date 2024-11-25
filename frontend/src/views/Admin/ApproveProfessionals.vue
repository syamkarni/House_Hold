<template>
    <div>
      <h2>Approve Professionals</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Service Type</th>
            <th>Experience</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="professional in professionals" :key="professional.id">
            <td>{{ professional.name }}</td>
            <td>{{ professional.service_type }}</td>
            <td>{{ professional.experience }}</td>
            <td>{{ professional.description }}</td>
            <td>
              <button @click="approveProfessional(professional.id)">Approve</button>
              <button @click="rejectProfessional(professional.id)">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="error" style="color: red;">{{ error }}</div>
    </div>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'ApproveProfessionals',
    data() {
      return {
        professionals: [],
        error: null,
      };
    },
    created() {
      this.fetchProfessionals();
    },
    methods: {
      async fetchProfessionals() {
        this.error = null;
        try {
          const response = await axios.get('/admin/professionals/pending', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          });
          this.professionals = response.data.professionals;
        } catch (error) {
          this.error = 'Error fetching professionals.';
          console.error('Error fetching professionals:', error);
        }
      },
      async approveProfessional(professionalId) {
        try {
          await axios.put(
            `/admin/professional/${professionalId}/approve`,
            {},
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              },
            }
          );
          this.fetchProfessionals();
        } catch (error) {
          console.error('Error approving professional:', error);
        }
      },
      async rejectProfessional(professionalId) {
        try {
          await axios.delete(
            `/admin/professional/${professionalId}/reject`,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              },
            }
          );
          this.fetchProfessionals();
        } catch (error) {
          console.error('Error rejecting professional:', error);
        }
      },
    },
  };
  </script>
  