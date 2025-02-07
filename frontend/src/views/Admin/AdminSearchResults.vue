<template>
    <div>
      <h2>Admin Search Results</h2>
  
      <div v-if="results && results.length && category === 'user'">
        <h3>Users</h3>
        <div v-for="user in results" :key="user.user_id" class="result-item">
          <p>User ID: {{ user.user_id }}</p>
          <p>Email: {{ user.u_mail }}</p>
          <p>Active: {{ user.is_active }}</p>
          <p>Roles: {{ user.roles.join(', ') }}</p>
          <hr />
        </div>
      </div>
  
      <div v-else-if="results && results.length && category === 'professional'">
        <h3>Professionals</h3>
        <div v-for="pro in results" :key="pro.id" class="result-item">
          <p>Professional ID: {{ pro.id }}</p>
          <p>Name: {{ pro.name }}</p>
          <p>Approved: {{ pro.approved }}</p>
          <p>Experience: {{ pro.experience }}</p>
          <p>Description: {{ pro.description }}</p>
          <p>Blocked: {{ pro.is_blocked }}</p>
          <hr />
        </div>
      </div>
  
      <div v-else-if="results && results.length && category === 'service'">
        <h3>Services</h3>
        <div v-for="svc in results" :key="svc.id" class="result-item">
          <p>Service ID: {{ svc.id }}</p>
          <p>Name: {{ svc.name }}</p>
          <p>Price: {{ svc.price }}</p>
          <p>Description: {{ svc.description }}</p>
          <p>Time Required: {{ svc.time_required }}</p>
          <hr />
        </div>
      </div>
  
      <div v-else-if="searchExecuted && (!results || !results.length)">
        <h4>No results found.</h4>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'AdminSearchResults',
    data() {
      return {
        category: '',
        searchTerm: '',
        results: null,
        searchExecuted: false
      };
    },
    async created() {
      this.category = this.$route.query.category || 'user';
      this.searchTerm = this.$route.query.searchTerm || '';
  
      await this.performSearch();
    },
    watch: {
      '$route.query': {
        immediate: false,
        handler() {
          this.category = this.$route.query.category || 'user';
          this.searchTerm = this.$route.query.searchTerm || '';
          this.performSearch();
        }
      }
    },
    methods: {
      async performSearch() {
        try {
          const token = localStorage.getItem('access_token');
          const response = await axios.get('/admin/search', {
            params: {
              category: this.category,
              searchTerm: this.searchTerm
            },
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
  
          this.results = response.data.results;
          this.searchExecuted = true;
        } catch (error) {
          console.error("Admin search error:", error);
          this.searchExecuted = true;
          this.results = [];
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
  