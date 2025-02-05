<template>
    <div>
      <h2>Customer Search</h2>
  
      <label for="category">Search Category:</label>
      <select id="category" v-model="searchCategory">
        <option value="services">Services</option>
        <option value="packages">Packages</option>
      </select>
  
      <label for="searchTerm">Search Term:</label>
      <input
        type="text"
        id="searchTerm"
        v-model="searchTerm"
        placeholder="Enter keyword..."
      />
  
      <button @click="performSearch">Search</button>
  
      <div v-if="searchCategory === 'services' && serviceResults.length">
        <h3>Found Services</h3>
        <div
          v-for="svc in serviceResults"
          :key="svc.id"
          class="result-item"
        >
          <p><strong>{{ svc.name }}</strong> (ID: {{ svc.id }})</p>
          <p>Description: {{ svc.description }}</p>
          <p>Base Price: {{ svc.base_price }}</p>
          <p>Time Required: {{ svc.time_required }}</p>
  
          <h4>Packages:</h4>
          <ul v-if="svc.packages && svc.packages.length">
            <li v-for="p in svc.packages" :key="p.id">
              {{ p.name }} - ${{ p.price }} ({{ p.time_required }} mins)
            </li>
          </ul>
          <hr/>
        </div>
      </div>
  
      <div v-else-if="searchCategory === 'packages' && packageResults.length">
        <h3>Found Packages</h3>
        <div
          v-for="pkg in packageResults"
          :key="pkg.id"
          class="result-item"
        >
          <p><strong>{{ pkg.name }}</strong> (ID: {{ pkg.id }})</p>
          <p>Description: {{ pkg.description }}</p>
          <p>Price: {{ pkg.price }}</p>
          <p>Time Required: {{ pkg.time_required }}</p>
          <p v-if="pkg.service">Attached to Service: {{ pkg.service.name }} (ID: {{ pkg.service.id }})</p>
          <hr/>
        </div>
      </div>
  
      <div v-else-if="searchExecuted && !serviceResults.length && !packageResults.length">
        <h4>No results found.</h4>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'CustomerSearch',
    data() {
      return {
        searchCategory: 'services',
        searchTerm: '',
        serviceResults: [],
        packageResults: [],
        searchExecuted: false
      };
    },
    methods: {
      async performSearch() {
        try {
          const token = localStorage.getItem('access_token');
          const response = await axios.get('/customer/search', {
            headers: {
              Authorization: `Bearer ${token}`
            },
            params: {
              category: this.searchCategory,
              searchTerm: this.searchTerm
            }
          });
  
          this.searchExecuted = true;
  
          this.serviceResults = [];
          this.packageResults = [];
  
          if (this.searchCategory === 'services' && response.data.services) {
            this.serviceResults = response.data.services;
          } else if (this.searchCategory === 'packages' && response.data.packages) {
            this.packageResults = response.data.packages;
          }
        } catch (error) {
          console.error("Search error:", error);
          this.searchExecuted = true;
          this.serviceResults = [];
          this.packageResults = [];
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .result-item {
    margin-bottom: 1rem;
  }
  </style>
  