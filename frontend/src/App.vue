<template>
  <div id="app">
    <AppNavbar />
    <router-view></router-view>
  </div>
</template>

<script>
import AppNavbar from './components/AppNavbar.vue';

export default {
  name: "App",
  components: {
    AppNavbar,
  },
};
</script>

<style>
/* Add any styles here */
</style>
