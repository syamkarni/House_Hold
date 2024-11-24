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

router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth;
  const userRole = localStorage.getItem('userRole');
  const isAuthentiacted = !!localStorage.getItem('access_token');

  if(requiresAuth){
    if(isAuthentiacted){
      if(to.meta.role==userRole){
        next();
      } else{
        next('/login');
      }
    } else{
      next('/login');
    }
  } else{
    next();
  }
});


export default router;
