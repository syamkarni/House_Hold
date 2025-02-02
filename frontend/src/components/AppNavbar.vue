<template>
  <nav>
    <ul>
      <li v-if="!authState.isAuthenticated">
        <router-link to="/login">Login</router-link>
      </li>
      <li v-if="!authState.isAuthenticated">
        <router-link to="/register">Register</router-link>
      </li>
      <li v-if="authState.isAuthenticated">
        <a href="#" @click.prevent="logoutUser">Logout</a>
      </li>
      <li v-if="authState.isAuthenticated && authState.userRole === 'admin'">
        <router-link to="/admin">Admin Dashboard</router-link>
      </li>
      <li v-if="authState.isAuthenticated && authState.userRole === 'professional'">
        <router-link to="/professional">Professional Dashboard</router-link>
      </li>
      <li v-if="authState.isAuthenticated && authState.userRole === 'customer'">
        <router-link to="/customer">Customer Dashboard</router-link>
      </li>
      <li v-if="authState.isAuthenticated">
        <select v-model="searchBy">
          <option v-for="option in searchOptions" :value="option.value" :key="option.value">
            {{ option.text }}
          </option>
        </select>
        <div v-if="searchBy === 'date_of_request'">
          <input type="date" v-model="dateFrom" placeholder="From" />
          <input type="date" v-model="dateTo" placeholder="To" />
        </div>
        <div v-else>
          <input type="text" v-model="searchText" placeholder="Enter search keyword" />
        </div>
        <button @click="performSearch">Search</button>
      </li>
    </ul>
  </nav>
</template>

<script>
import { authState, logout } from '@/services/auth';
import { useRouter } from 'vue-router';
import axios from '@/plugins/axios';

export default {
  data() {
    return {
      searchBy: '',
      searchText: '',
      dateFrom: '',
      dateTo: '',
      searchOptions: [],
    };
  },
  mounted() {
    this.setSearchOptions(authState.userRole);
  },
  methods: {
    setSearchOptions(role) {
      if (role === 'admin') {
        this.searchOptions = [
          { value: 'customer', text: 'Customer' },
          { value: 'professional', text: 'Professional' },
          { value: 'service', text: 'Service' }
        ];
      } else if (role === 'professional') {
        this.searchOptions = [
          { value: 'service', text: 'Service' },
          { value: 'date_of_request', text: 'Date of Request' },
          { value: 'customer_remarks', text: 'Customer Remarks' }
        ];
      } else if (role === 'customer') {
        this.searchOptions = [
          { value: 'services', text: 'Services' },
          { value: 'packages', text: 'Packages' }
        ];
      }
      if (this.searchOptions.length) {
        this.searchBy = this.searchOptions[0].value;
      }
    },
    async performSearch() {
      const role = authState.userRole;
      let params = { search_by: this.searchBy };

      if (this.searchBy === 'date_of_request') {
        if (this.dateFrom) params.date_from = this.dateFrom;
        if (this.dateTo) params.date_to = this.dateTo;
      } else {
        if (this.searchText.trim() === '') {
          alert('Please enter a search keyword.');
          return;
        }
        params.search_text = this.searchText.trim();
      }

      try {
        const response = await axios.get('/search', {
          params,
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        });

        this.router.push({
          name: 'SearchResults',
          params: { role },
          query: { results: JSON.stringify(response.data.results) }
        });

      } catch (error) {
        console.error('Error during search:', error);
        alert('An error occurred while performing the search.');
      }
    },
    logoutUser() {
      logout();
      window.location.href = '/login';
    }
  },
  setup() {
    const router = useRouter();
    return {
      authState,
      router
    };
  }
};
</script>
