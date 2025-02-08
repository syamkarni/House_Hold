<template>
    <div>
      <label for="searchCategory">Search Category:</label>
      <select v-model="searchCategory" id="searchCategory">
        <option value="service">Service</option>
        <option value="date_of_request">Date of Request</option>
        <option value="customer_remarks">Customer Remarks</option>
      </select>
  
      <div v-if="searchCategory === 'service' || searchCategory === 'customer_remarks'">
        <label for="searchTerm">Search Term:</label>
        <input
          type="text"
          id="searchTerm"
          v-model="searchTerm"
          placeholder="Enter keyword..."
        />
      </div>
  
      <div v-if="searchCategory === 'date_of_request'">
        <label>From Date:</label>
        <input type="date" v-model="fromDate" />
        <label>To Date:</label>
        <input type="date" v-model="toDate" />
      </div>
  
      <button @click="goToSearchResults">Search</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ProfessionalSearchBar',
    data() {
      return {
        searchCategory: 'service',
        searchTerm: '',
        fromDate: '',
        toDate: ''
      };
    },
    methods: {
      goToSearchResults() {
        const query = { category: this.searchCategory };
  
        if (this.searchCategory === 'service' || this.searchCategory === 'customer_remarks') {
          query.searchTerm = this.searchTerm;
        } else if (this.searchCategory === 'date_of_request') {
          query.fromDate = this.fromDate;
          query.toDate = this.toDate;
        }
  
        this.$router.push({
          name: 'ProfessionalSearchResults',
          query
        });
      }
    }
  };
  </script>
  