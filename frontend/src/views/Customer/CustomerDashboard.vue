<template>
    <div>
      <h1>Customer Dashboard</h1>
      <p>Welcome, Customer!</p>
      <!-- yup functionalities here too!!! -->
      <nav>
      <ul>
        <li><router-link to="/customer/services">View Available Services</router-link></li>
        <li><router-link to="/customer/service_requests">View Service History</router-link></li>
        <!-- <li>
          <router-link
            :to="{ name: 'ProvideReview', params: { requestId: 1 } }"
          >
            Provide Review for a Service Request (Sample ID: 1)
          </router-link>
        </li> -->
        <!-- <li><router-link to="/customer/search">Search (Services/Packages)</router-link></li> -->
      </ul>
    </nav>


    <router-view></router-view>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CustomerDashboard',
    created() {
    },
  };
  </script>
  