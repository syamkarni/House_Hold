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
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path:'/customer',
    component: CustomerDashboard,
    meta: { requiresAuth: true, role: "customer" },
  },
  {
    path:'/professional',
    component: ProfessionalDashboard,
    meta: { requiresAuth: true, role: "professional" },
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth;
  const userRole = localStorage.getItem('user_role');
  const isAuthenticated = !!localStorage.getItem('access_token');
  //debugging
  console.log("Navigating to:", to.path);
  console.log("Requires Auth:", requiresAuth);
  console.log("User Role:", userRole);
  console.log("Is Authenticated:", isAuthenticated);

  if(requiresAuth){
    if(isAuthenticated){
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
