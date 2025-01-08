<template>
    <div>
      <h2>Provide Review</h2>
      <div v-if="error" style="color: red;">{{ error }}</div>
      <form @submit.prevent="submitReview">
        <div>
          <label for="rating">Rating (1-5):</label>
          <input id="rating" type="number" v-model.number="rating" min="1" max="5" required />
        </div>
        <div>
          <label for="comment">Comment:</label>
          <textarea id="comment" v-model="comment"></textarea>
        </div>
        <button type="submit">Submit Review</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'ProvideReview',
    data() {
      return {
        rating: 5,
        comment: '',
        error: null,
      };
    },
    methods: {
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
    },
  };
  </script>
  