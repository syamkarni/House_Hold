<template>
    <div>
      <h2>Manage Users</h2>
      <table>
        <thead>
          <tr>
            <th>Email</th>
            <th>Roles</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.user_id">
            <td>{{ user.u_mail }}</td>
            <td>{{ user.roles.join(', ') }}</td>
            <td>{{ user.is_blocked ? 'Blocked' : 'Active' }}</td>
            <td>
              <button @click="blockUser(user.user_id)" v-if="!user.is_blocked">Block</button>
              <button @click="unblockUser(user.user_id)" v-if="user.is_blocked">Unblock</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="error" style="color: red;">{{ error }}</div>
    </div>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'ManageUsers',
    data() {
      return {
        users: [],
        error: null,
      };
    },
    created() {
      this.fetchUsers();
    },
    methods: {
      async fetchUsers() {
        this.error = null;
        try {
          const response = await axios.get('/admin/users', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          });
          this.users = response.data.users;
        } catch (error) {
          this.error = 'Error fetching users.';
          console.error('Error fetching users:', error);
        }
      },
      async blockUser(userId) {
        try {
          await axios.put(
            `/admin/user/${userId}/block`,
            {},
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              },
            }
          );
          this.fetchUsers();
        } catch (error) {
          console.error('Error blocking user:', error);
        }
      },
      async unblockUser(userId) {
        try {
          await axios.put(
            `/admin/user/${userId}/unblock`,
            {},
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              },
            }
          );
          this.fetchUsers();
        } catch (error) {
          console.error('Error unblocking user:', error);
        }
      },
    },
  };
  </script>
  