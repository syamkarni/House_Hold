<template>
    <div>
      <h2>Admin Search</h2>
  
      <label for="category">Search Category:</label>
      <select id="category" v-model="selectedCategory">
        <option value="user">User</option>
        <option value="professional">Professional</option>
        <option value="service">Service</option>
      </select>
  
      <label for="searchTerm">Search Term:</label>
      <input
        type="text"
        id="searchTerm"
        v-model="searchTerm"
        placeholder="Enter keyword..."
      />
  
      <button @click="performSearch">Search</button>
  
      <div class="search-results" v-if="results && results.length">
        <h3>Results ({{ selectedCategory }})</h3>
  
        <div v-if="selectedCategory === 'user'">
          <div
            v-for="user in results"
            :key="user.user_id"
            class="result-item"
          >
            <p>User ID: {{ user.user_id }}</p>
            <p>Email: {{ user.u_mail }}</p>
            <p>Active: {{ user.is_active }}</p>
            <p>Roles: {{ user.roles.join(', ') }}</p>
            <hr />
          </div>
        </div>
        <div v-if="selectedCategory === 'professional'">
          <div
            v-for="pro in results"
            :key="pro.id"
            class="result-item"
          >
            <p>Professional ID: {{ pro.id }}</p>
            <p>Name: {{ pro.name }}</p>
            <p>Approved: {{ pro.approved }}</p>
            <p>Experience: {{ pro.experience }}</p>
            <p>Description: {{ pro.description }}</p>
            <p>Blocked: {{ pro.is_blocked }}</p>
            <hr />
          </div>
        </div>
  
        <div v-if="selectedCategory === 'service'">
          <div
            v-for="service in results"
            :key="service.id"
            class="result-item"
          >
            <p>Service ID: {{ service.id }}</p>
            <p>Name: {{ service.name }}</p>
            <p>Price: {{ service.price }}</p>
            <p>Description: {{ service.description }}</p>
            <p>Time Required: {{ service.time_required }}</p>
            <hr />
          </div>
        </div>
      </div>
  
      <div v-else-if="results && !results.length">
        <h4>No results found.</h4>
      </div>
    </div>
  </template>
  
  <script>
  import api from '@/plugins/axios';
  
  export default {
    name: "AdminSearch",
    data() {
      return {
        selectedCategory: 'user',
        searchTerm: '',
        results: null
      };
    },
    methods: {
      async performSearch() {
        try {
          const token = localStorage.getItem('access_token');
  
          const response = await api.get('/admin/search', {
            params: {
              category: this.selectedCategory,
              searchTerm: this.searchTerm
            },
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          this.results = response.data.results;
        } catch (error) {
          console.error("Search error:", error);
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
  