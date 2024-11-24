import { createRouter, createWebHistory } from 'vue-router';
import AuthLogin from '@/views/Auth/AuthLogin.vue';
import AuthRegister from '@/views/Auth/AuthRegister.vue';

const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    component: AuthLogin,
  },
  {
    path: '/register',
    component: AuthRegister,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
