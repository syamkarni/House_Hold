<template>
    <div>
      <h2>Manage Services</h2>
      <button @click="showCreateForm = true">Add New Service</button>
  

      <div v-if="showCreateForm">
        <h3>Create Service</h3>
        <form @submit.prevent="createService">
          <div>
            <label>Name:</label>
            <input type="text" v-model="newService.name" required />
          </div>
          <div>
            <label>Price:</label>
            <input type="number" v-model="newService.price" required />
          </div>
          <div>
            <label>Time Required (minutes):</label>
            <input type="number" v-model="newService.time_required" required />
          </div>
          <div>
            <label>Description:</label>
            <textarea v-model="newService.description" required></textarea>
          </div>
          <button type="submit">Create Service</button>
          <button @click="showCreateForm = false">Cancel</button>
        </form>
      </div>
  
      <!-- Services List -->
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Price</th>
            <th>Time Required</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in services" :key="service.id">
            <td>{{ service.name }}</td>
            <td>{{ service.price }}</td>
            <td>{{ service.time_required }}</td>
            <td>{{ service.description }}</td>
            <td>
              <button @click="editService(service)">Edit</button>
              <button @click="deleteService(service.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Edit Service Form -->
      <div v-if="showEditForm">
        <h3>Edit Service</h3>
        <form @submit.prevent="updateService">
          <div>
            <label>Name:</label>
            <input type="text" v-model="editServiceData.name" required />
          </div>
          <div>
            <label>Price:</label>
            <input type="number" v-model="editServiceData.price" required />
          </div>
          <div>
            <label>Time Required (minutes):</label>
            <input type="number" v-model="editServiceData.time_required" required />
          </div>
          <div>
            <label>Description:</label>
            <textarea v-model="editServiceData.description" required></textarea>
          </div>
          <button type="submit">Update Service</button>
          <button @click="showEditForm = false">Cancel</button>
        </form>
      </div>
  
      <div v-if="error" style="color: red;">{{ error }}</div>
    </div>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'ManageServices',
    data() {
      return {
        services: [],
        showCreateForm: false,
        showEditForm: false,
        newService: {
          name: '',
          price: 0,
          time_required: 0,
          description: '',
        },
        editServiceData: {},
        error: null,
      };
    },
    created() {
      this.fetchServices();
    },
    methods: {
      async fetchServices() {
        this.error = null;
        try {
          const response = await axios.get('/services', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          });
          this.services = response.data.services;
        } catch (error) {
          this.error = 'Error fetching services.';
          console.error('Error fetching services:', error);
        }
      },
      async createService() {
        try {
          await axios.post(
            '/admin/service',
            this.newService,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              },
            }
          );
          this.fetchServices();
          this.showCreateForm = false;
          // Reset form
          this.newService = {
            name: '',
            price: 0,
            time_required: 0,
            description: '',
          };
        } catch (error) {
          this.error = 'Error creating service.';
          console.error('Error creating service:', error);
        }
      },
      editService(service) {
        this.editServiceData = { ...service };
        this.showEditForm = true;
      },
      async updateService() {
        try {
          await axios.put(
            `/admin/service/${this.editServiceData.id}`,
            this.editServiceData,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              },
            }
          );
          this.fetchServices();
          this.showEditForm = false;
        } catch (error) {
          this.error = 'Error updating service.';
          console.error('Error updating service:', error);
        }
      },
      async deleteService(serviceId) {
        try {
          await axios.delete(`/admin/service/${serviceId}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          });
          this.fetchServices();
        } catch (error) {
          this.error = 'Error deleting service.';
          console.error('Error deleting service:', error);
        }
      },
    },
  };
  </script>
  