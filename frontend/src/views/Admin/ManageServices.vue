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
      <div v-if="services.length">
      <div v-for="service in services" :key="service.id" class="service-card">
        <h3>{{ service.name }}</h3>
        <p><strong>Average Price:</strong> {{ service.price }}</p>
        <p><strong>Average Time Required:</strong> {{ service.time_required }}</p>
        <p><strong>Description:</strong> {{ service.description }}</p>
        <div>
          <strong>Packages:</strong>
          <table v-if="service.packages && service.packages.length">
            <thead>
              <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Price</th>
                <th>Time Required (mins)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="pkg in service.packages" :key="pkg.id">
                <td>{{ pkg.name }}</td>
                <td>{{ pkg.description }}</td>
                <td>${{ pkg.price }}</td>
                <td>{{ pkg.time_required }}</td>
              </tr>
            </tbody>
          </table>
          <span v-else>No packages found for this service</span>
        </div>
        <div>
          <!-- <button @click="editService(service)">Edit</button> -->
          <button @click="$router.push({ name: 'EditService', params: { id: service.id } })">
            Edit
          </button>
          <button @click="deleteService(service.id)">Delete</button>
        </div>
      </div>
    </div>
    <div v-else>
      <p>No services found.</p>
    </div>
  
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
          const response = await axios.get('/admin/services', {
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
  