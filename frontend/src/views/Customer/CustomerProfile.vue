<script>
import axios from '@/plugins/axios';
import { authState } from '@/services/auth';

export default {
  name: 'CustomerProfile',
  data() {
    return {
      name: '',
      phone: '',
      address: '',
      message: '',
      success: false,
    };
  },
  created() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await axios.get('/customer/profile', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        });
        const profile = response.data.profile;
        this.name = profile.name || '';
        this.phone = profile.phone || '';
        this.address = profile.address || '';
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
    async updateProfile() {
      try {
        await axios.put(
          '/customer/profile',
          {
            name: this.name,
            phone: this.phone,
            address: this.address,
          },
          {
            headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
          }
        );
        this.message = 'Profile updated successfully.';
        this.success = true;

        authState.profileComplete = true;
        localStorage.setItem('profile_complete', 'true');

        this.$router.push('/customer');
      } catch (error) {
        console.error('Error updating profile:', error);
        this.message = 'Failed to update profile.';
        this.success = false;
      }
    },
  },
};
</script>
