<template>
  <div>
    <h1>Login</h1>
    <LoginForm />
  </div>
</template>

<script>
import LoginForm from '@/components/Auth/LoginForm.vue';

export default {
  name: 'AuthLogin',
  components: {
    LoginForm,
  },
};
</script>
