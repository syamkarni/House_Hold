<template>
    <div>
      <h2>Professional Search</h2>
  
      <!-- Category Dropdown -->
      <label for="searchCategory">Search Category:</label>
      <select v-model="searchCategory" id="searchCategory">
        <option value="service">Service</option>
        <option value="date_of_request">Date of Request</option>
        <option value="customer_remarks">Customer Remarks</option>
      </select>
  
      <!-- For 'service' or 'customer_remarks' => single text input -->
      <div v-if="searchCategory === 'service' || searchCategory === 'customer_remarks'">
        <label for="searchTerm">Search Term:</label>
        <input
          type="text"
          id="searchTerm"
          v-model="searchTerm"
          placeholder="Enter keyword..."
        />
      </div>
  
      <!-- For 'date_of_request' => two date fields -->
      <div v-if="searchCategory === 'date_of_request'">
        <label>From Date:</label>
        <input type="date" v-model="fromDate" />
        <label>To Date:</label>
        <input type="date" v-model="toDate" />
      </div>
  
      <!-- Search Button -->
      <button @click="performSearch">Search</button>
  
      <!-- Results Table -->
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
  
      <!-- No results -->
      <div v-else-if="results && !results.length">
        <h4>No results found.</h4>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'ProfessionalSearch',
    data() {
      return {
        searchCategory: 'service', // Default category
        searchTerm: '',
        fromDate: '',
        toDate: '',
        results: null,
      };
    },
    methods: {
      async performSearch() {
        try {
          const token = localStorage.getItem('access_token');
          const params = { category: this.searchCategory };
  
          // If searching by service or remarks
          if (this.searchCategory === 'service' || this.searchCategory === 'customer_remarks') {
            params.searchTerm = this.searchTerm;
          }
          // If searching by date range
          else if (this.searchCategory === 'date_of_request') {
            params.fromDate = this.fromDate;
            params.toDate = this.toDate;
          }
  
          const response = await axios.get('/professional/search', {
            headers: { Authorization: `Bearer ${token}` },
            params
          });
          // Suppose the backend returns { "requests": [...] }
          this.results = response.data.requests;
        } catch (error) {
          console.error("Search error:", error);
          this.results = [];
        }
      },
      formatDate(isoString) {
        // Basic helper to parse an ISO date into a readable format
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
  