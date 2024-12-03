<template>
  <div>
    <h1>Professional Dashboard</h1>
    <div v-if="!approved">
      <p>Your profile is pending approval.</p>
      <router-link to="/professional/pending-approval">View Status</router-link>
    </div>
    <div v-else>
      <!-- Dashboard content -->
      <ul>
        <li><router-link to="/professional/assigned-requests">Assigned Requests</router-link></li>
      </ul>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import axios from '@/plugins/axios';

export default {
  name: 'ProfessionalDashboard',
  data() {
    return {
      approved: false,
    };
  },
  created() {
    this.checkApproval();
  },
  methods: {
    async checkApproval() {
      try {
        const response = await axios.get('/professional/profile', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        });
        this.approved = response.data.profile.approved;

        if (!this.approved && this.$route.path !== '/professional/pending-approval') {
          this.$router.push('/professional/pending-approval');
        }
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
  },
};
</script>

<style scoped>

</style>
