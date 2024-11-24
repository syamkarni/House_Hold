<template>
    <div>
      <h1>Register</h1>
      <RegisterForm />
    </div>
  </template>
  
  <script>
  import RegisterForm from '@/components/Auth/RegisterForm.vue';
  
  export default {
    name: 'AuthRegister',
    components: {
      RegisterForm,
    },
  };
  </script>
  