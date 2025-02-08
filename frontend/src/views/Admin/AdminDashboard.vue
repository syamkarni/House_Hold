<template>
    <div>
      <h1>Admin Dashboard</h1>
      <p>Welcome, Admin!</p>
      <!-- need to add functionities here!! -->
      <ul>
        <li><router-link to="/admin/manage-users">Manage Users</router-link></li>
        <li><router-link to="/admin/manage-services">Manage Services</router-link></li>
        <li><router-link to="/admin/approve-professionals">Approve Professionals</router-link></li>
        <li><router-link to="/admin/admin-reports">Reports</router-link></li>
        <!-- <li><router-link to="/admin/search">Search</router-link></li> -->
    </ul> 
    <router-view />
    </div>
  </template>
  
  <script>
  export default {
    name: 'AdminDashboard',
    created() {

    },
  };
  </script>
  