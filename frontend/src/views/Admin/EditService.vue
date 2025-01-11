<template>
  <div>
    <h2>Edit Service</h2>
    <div v-if="error" style="color: red;">{{ error }}</div>
    <div v-if="service">
      <form @submit.prevent="updateService">
        <div>
          <label>Name:</label>
          <input type="text" v-model="service.name" required />
        </div>
        <div>
          <label>Avg Price:</label>
          <input type="number" v-model.number="service.price" required />
        </div>
        <div>
          <label>Avg Time Required (minutes):</label>
          <input type="number" v-model.number="service.time_required" required />
        </div>
        <div>
          <label>Description:</label>
          <textarea v-model="service.description" required></textarea>
        </div>
        <button type="submit">Update Service</button>
        <button type="button" @click="$router.back()">Cancel</button>
      </form>

      <h3>Packages for {{ service.name }}</h3>
      <div v-if="service.packages && service.packages.length">
        <ul>
          <li v-for="pkg in service.packages" :key="pkg.id">
            {{ pkg.name }} - ${{ pkg.price }} - {{ pkg.time_required }} mins
            <button @click="editPackage(pkg)">Edit</button>
            <button @click="deletePackage(pkg.id)">Delete</button>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No packages available for this service.</p>
      </div>

      <button @click="showAddPackageForm = true">Add New Package</button>

      <div v-if="showAddPackageForm">
        <h4>Add Package</h4>
        <form @submit.prevent="createPackage">
          <div>
            <label>Name:</label>
            <input type="text" v-model="newPackage.name" required />
          </div>
          <div>
            <label>Description:</label>
            <textarea v-model="newPackage.description" required></textarea>
          </div>
          <div>
            <label>Price:</label>
            <input type="number" v-model.number="newPackage.price" required />
          </div>
          <div>
            <label>Time Required (minutes):</label>
            <input type="number" v-model.number="newPackage.time_required" required />
          </div>
          <button type="submit">Create Package</button>
          <button type="button" @click="showAddPackageForm = false">Cancel</button>
        </form>
      </div>
      <div v-if="showEditPackageForm">
        <h4>Edit Package</h4>
        <form @submit.prevent="updatePackage">
          <div>
            <label>Name:</label>
            <input type="text" v-model="editingPackage.name" required />
          </div>
          <div>
            <label>Description:</label>
            <textarea v-model="editingPackage.description" required></textarea>
          </div>
          <div>
            <label>Price:</label>
            <input type="number" v-model.number="editingPackage.price" required />
          </div>
          <div>
            <label>Time Required (minutes):</label>
            <input type="number" v-model.number="editingPackage.time_required" required />
          </div>
          <button type="submit">Update Package</button>
          <button type="button" @click="cancelEditPackage">Cancel</button>
        </form>
      </div>

    </div>
    <div v-else>
      <p>Loading service details...</p>
    </div>
  </div>
</template>
  
  <script>
import axios from '@/plugins/axios';

export default {
  name: 'EditService',
  data() {
    return {
      service: null,
      error: null,
      showAddPackageForm: false,
      showEditPackageForm: false,
      newPackage: {
        name: '',
        description: '',
        price: 0,
        time_required: 0,
      },
      editingPackage: null,
    };
  },
  async created() {
    const serviceId = this.$route.params.id;
    try {
      const response = await axios.get('/admin/services', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      });
      const services = response.data.services;
      this.service = services.find(s => s.id === parseInt(serviceId));
      if (!this.service) {
        this.error = 'Service not found';
      }
    } catch (err) {
      this.error = 'Error fetching service details.';
      console.error(err);
    }
  },
  methods: {
    async updateService() {
      try {
        await axios.put(
          `/admin/service/${this.service.id}`,
          this.service,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          }
        );
        this.$router.push({ name: 'ManageServices' });
      } catch (error) {
        this.error = 'Error updating service.';
        console.error('Error updating service:', error);
      }
    },
    editPackage(pkg) {
    this.editingPackage = { ...pkg };
    this.showEditPackageForm = true;
  },

  async updatePackage() {
    try {
      await axios.put(
        `/admin/package/${this.editingPackage.id}`,
        this.editingPackage,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        }
      );
      this.showEditPackageForm = false;
      this.editingPackage = null;
      await this.fetchServiceDetails(this.service.id);
    } catch (error) {
      this.error = 'Error updating package.';
      console.error(error);
    }
  },

  cancelEditPackage() {
    this.showEditPackageForm = false;
    this.editingPackage = null;
  },
    async createPackage() {
      try {
        await axios.post(
          `/admin/service/${this.service.id}/package`,
          this.newPackage,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          }
        );
        await this.fetchServiceDetails(this.service.id);
        this.showAddPackageForm = false;
        this.newPackage = { name: '', description: '', price: 0, time_required: 0 };
      } catch (error) {
        this.error = 'Error creating package.';
        console.error(error);
      }
    },
    async deletePackage(packageId) {
      try {
        await axios.delete(`/admin/package/${packageId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        await this.fetchServiceDetails(this.service.id);
      } catch (error) {
        this.error = 'Error deleting package.';
        console.error(error);
      }
    },
    async fetchServiceDetails(serviceId) {
      try {
        const response = await axios.get('/admin/services', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        const services = response.data.services;
        this.service = services.find(s => s.id === parseInt(serviceId));
      } catch (error) {
        this.error = 'Error fetching service details.';
        console.error(error);
      }
    },
  },
};
</script>
