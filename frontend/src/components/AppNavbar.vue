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
      <li v-if="authState.isAuthenticated && authState.userRole === 'customer'">
        <router-link to="/customer">Customer Dashboard</router-link>
        <router-link to="/customer/profile">Profile</router-link>
      </li>
      <li v-if="authState.isAuthenticated && authState.userRole === 'professional'">
        <router-link to="/professional">Professional Dashboard</router-link>
      </li>
    </ul>
    <div v-if="authState.isAuthenticated && authState.userRole === 'customer'">
      <CustomerSearchBar />
    </div>

    <div v-if="authState.isAuthenticated && authState.userRole === 'admin'">
      <AdminSearchBar />
    </div>
    <div v-if="authState.isAuthenticated && authState.userRole == 'professional'">
      <ProfessionalSearchBar />
    </div>
  </nav>
</template>

<script>
import { authState, logout } from '@/services/auth';
import CustomerSearchBar from '@/views/Customer/CustomerSearchBar.vue';
import AdminSearchBar from '@/views/Admin/AdminSearchBar.vue';
import ProfessionalSearchBar from '@/views/Professional/ProfessionalSearchBar.vue';

export default {
  name: 'AppNavbar',
  components: {
    CustomerSearchBar,
    AdminSearchBar,
    ProfessionalSearchBar
  },
  setup() {
    const logoutUser = () => {
      logout();
      window.location.href = '/login';
    };

    return {
      authState,
      logoutUser,
    };
  },
};
</script>