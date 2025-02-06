<template>
    <div>
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
  
      <button @click="goToSearchResults">Search</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CustomerSearchBar',
    data() {
      return {
        searchCategory: 'services',
        searchTerm: '',
      };
    },
    methods: {
      goToSearchResults() {
        this.$router.push({
          name: 'CustomerSearchResults',
          query: {
            category: this.searchCategory,
            searchTerm: this.searchTerm
          }
        });
      }
    }
  };
  </script>
  