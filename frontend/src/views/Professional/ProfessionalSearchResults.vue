<template>
    <div>
      <h2>Professional Search Results</h2>
  
      <div v-if="results && results.length">
        <h3>Search Results</h3>
        <table>
          <thead>
            <tr>
              <th>Request ID</th>
              <th>Service Name</th>
              <th>Date of Request</th>
              <th>Customer Remarks</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="req in results" :key="req.id">
              <td>{{ req.id }}</td>
              <td>{{ req.service ? req.service.name : 'N/A' }}</td>
              <td>{{ formatDate(req.date_of_request) }}</td>
              <td>{{ req.remarks }}</td>
              <td>{{ req.service_status }}</td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <div v-else-if="searchExecuted && (!results || !results.length)">
        <h4>No results found.</h4>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'ProfessionalSearchResults',
    data() {
      return {
        category: '',
        searchTerm: '',
        fromDate: '',
        toDate: '',
        results: null,
        searchExecuted: false
      };
    },
    async created() {
      this.category = this.$route.query.category || 'service';
      this.searchTerm = this.$route.query.searchTerm || '';
      this.fromDate = this.$route.query.fromDate || '';
      this.toDate = this.$route.query.toDate || '';
  
      await this.performSearch();
    },
    watch: {
      '$route.query': {
        immediate: false,
        handler() {
          this.category = this.$route.query.category || 'service';
          this.searchTerm = this.$route.query.searchTerm || '';
          this.fromDate = this.$route.query.fromDate || '';
          this.toDate = this.$route.query.toDate || '';
          this.performSearch();
        }
      }
    },
    methods: {
      async performSearch() {
        try {
          const token = localStorage.getItem('access_token');
          const params = { category: this.category };
  
          if (this.category === 'service' || this.category === 'customer_remarks') {
            params.searchTerm = this.searchTerm;
          } else if (this.category === 'date_of_request') {
            params.fromDate = this.fromDate;
            params.toDate = this.toDate;
          }
  
          const response = await axios.get('/professional/search', {
            headers: { Authorization: `Bearer ${token}` },
            params
          });
  
          this.results = response.data.requests;
          this.searchExecuted = true;
        } catch (error) {
          console.error("Professional search error:", error);
          this.searchExecuted = true;
          this.results = [];
        }
      },
      formatDate(isoString) {
        if (!isoString) return '';
        const date = new Date(isoString);
        return date.toLocaleDateString();
      }
    }
  };
  </script>
  
  <style scoped>
  table {
    border-collapse: collapse;
    margin-top: 1rem;
  }
  
  th, td {
    border: 1px solid #ccc;
    padding: 0.5rem;
  }
  </style>
  