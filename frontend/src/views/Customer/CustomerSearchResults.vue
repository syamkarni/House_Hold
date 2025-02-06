<template>
    <div>
      <h2>Search Results</h2>
  
      <div v-if="services && services.length && category === 'services'">
        <h3>Services</h3>
        <div v-for="svc in services" :key="svc.id" class="result-item">
          <strong>{{ svc.name }}</strong> (ID: {{ svc.id }})<br/>
          Description: {{ svc.description }}<br/>
          Base Price: {{ svc.base_price }}<br/>
          Time Required: {{ svc.time_required }}<br/>
          <h4>Packages:</h4>
          <ul>
            <li v-for="pkg in svc.packages" :key="pkg.id">
              {{ pkg.name }} - ${{ pkg.price }}
            </li>
          </ul>
          <hr/>
        </div>
      </div>
  
      <div v-if="packages && packages.length && category === 'packages'">
        <h3>Packages</h3>
        <div v-for="pkg in packages" :key="pkg.id" class="result-item">
          <strong>{{ pkg.name }}</strong> (ID: {{ pkg.id }})<br/>
          Description: {{ pkg.description }}<br/>
          Price: {{ pkg.price }}<br/>
          Time Required: {{ pkg.time_required }}<br/>
          Attached to service: {{ pkg.service ? pkg.service.name : 'N/A' }}
          <hr/>
        </div>
      </div>
  
      <div v-if="searchExecuted && !services.length && !packages.length">
        <p>No results found.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'CustomerSearchResults',
    data() {
      return {
        category: '',
        searchTerm: '',
        services: [],
        packages: [],
        searchExecuted: false
      };
    },
    async created() {
      this.category = this.$route.query.category || 'services';
      this.searchTerm = this.$route.query.searchTerm || '';
  

      await this.performSearch();
    },
    watch: {
      '$route.query': {
        immediate: false,
        handler() {
          this.category = this.$route.query.category || 'services';
          this.searchTerm = this.$route.query.searchTerm || '';
          this.performSearch();
        }
      }
    },
    methods: {
      async performSearch() {
        try {
          const token = localStorage.getItem('access_token');
          const response = await axios.get('/customer/search', {
            headers: { Authorization: `Bearer ${token}` },
            params: {
              category: this.category,
              searchTerm: this.searchTerm
            }
          });
  
          this.searchExecuted = true;
          this.services = [];
          this.packages = [];
  
          if (this.category === 'services' && response.data.services) {
            this.services = response.data.services;
          }
          else if (this.category === 'packages' && response.data.packages) {
            this.packages = response.data.packages;
          }
        } catch (error) {
          console.error("Search error:", error);
          this.searchExecuted = true;
          this.services = [];
          this.packages = [];
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
  