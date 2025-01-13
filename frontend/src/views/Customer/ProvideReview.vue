<template>
  <div>
    <h2>Provide Review</h2>
    <div v-if="error" style="color: red;">{{ error }}</div>
    
    <div v-if="requestDetails">
      <p><strong>Service:</strong> {{ requestDetails.service.name }}</p>
      <p><strong>Package:</strong> 
         <span v-if="requestDetails.package">{{ requestDetails.package.name }}</span>
         <span v-else>N/A</span>
      </p>
      <p><strong>Professional:</strong> 
         <span v-if="requestDetails.professional">{{ requestDetails.professional.name }}</span>
         <span v-else>Not Assigned</span>
      </p>
      <p><strong>Date of Request:</strong> {{ requestDetails.date_of_request }}</p>
    </div>
    
    <form @submit.prevent="submitReview">
      <div>
        <label for="rating">Rating:</label>
        <select id="rating" v-model.number="rating" required>
          <option disabled value="">Select a rating</option>
          <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
        </select>
      </div>
      <div>
        <label for="comment">Comment:</label>
        <textarea id="comment" v-model="comment"></textarea>
      </div>
      <button type="submit">Submit Review</button>
      <button type="button" @click="cancelReview">Cancel</button>
    </form>
  </div>
</template>

<script>
import axios from '@/plugins/axios';

export default {
  name: 'ProvideReview',
  data() {
    return {
      rating: null,         
      comment: '',
      error: null,
      requestDetails: null, 
    };
  },
  async created() {
    await this.fetchRequestDetails();
  },
  methods: {
    async fetchRequestDetails() {
      const requestId = this.$route.params.requestId;
      try {
        const response = await axios.get('/customer/service_requests', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        const requests = response.data.requests;
        this.requestDetails = requests.find(req => req.id === parseInt(requestId));
      } catch (error) {
        this.error = 'Error fetching request details.';
        console.error('Error fetching request details:', error);
      }
    },
    async submitReview() {
      const requestId = this.$route.params.requestId;
      try {
        await axios.post(
          `/customer/service_request/${requestId}/review`,
          {
            rating: this.rating,
            comment: this.comment,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          }
        );
        this.$router.push({ name: 'CustomerServiceRequests' });
      } catch (error) {
        this.error = 'Error submitting review.';
        console.error('Error submitting review:', error);
      }
    },
    cancelReview() {
      this.$router.push({ name: 'CustomerServiceRequests' });
    }
  },
};
</script>
