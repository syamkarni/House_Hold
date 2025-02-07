<template>
    <div>
      <label for="adminCategory">Search Category:</label>
      <select id="adminCategory" v-model="adminCategory">
        <option value="user">User</option>
        <option value="professional">Professional</option>
        <option value="service">Service</option>
      </select>
  
      <label for="adminSearchTerm">Search Term:</label>
      <input
        type="text"
        id="adminSearchTerm"
        v-model="adminSearchTerm"
        placeholder="Enter keyword..."
      />
  
      <button @click="goToSearchResults">Search</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AdminSearchBar',
    data() {
      return {
        adminCategory: 'user',
        adminSearchTerm: ''
      };
    },
    methods: {
      goToSearchResults() {
        this.$router.push({
          name: 'AdminSearchResults',
          query: {
            category: this.adminCategory,
            searchTerm: this.adminSearchTerm
          }
        });
      }
    }
  };
  </script>
  