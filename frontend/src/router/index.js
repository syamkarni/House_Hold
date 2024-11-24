import { createRouter, createWebHistory } from 'vue-router';
import AuthLogin from '@/views/Auth/AuthLogin.vue';
import AuthRegister from '@/views/Auth/AuthRegister.vue';
import AdminDashboard from '@/views/Admin/AdminDashboard.vue';
import CustomerDashboard from '@/views/Customer/CustomerDashboard.vue';
import ProfessionalDashboard from '@/views/Professional/ProfessionalDashboard.vue';

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
  {
    path:'/admin',
    component: AdminDashboard,
  },
  {
    path:'/customer',
    component: CustomerDashboard,
  },
  {
    path:'/professional',
    component: ProfessionalDashboard,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});



export default router;
