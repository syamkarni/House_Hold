<template>
    <div>
      <h1>Professional Dashboard</h1>
      <ul>
        <li><router-link to="/professional/assigned-requests">Assigned Requests</router-link></li>
      </ul>
      <router-view></router-view>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ProfessionalDashboard',
    created() {
    },
  };
  </script>
  