import { createRouter, createWebHistory } from 'vue-router';
import { authState } from '@/services/auth';
import AuthLogin from '@/views/Auth/AuthLogin.vue';
import AuthRegister from '@/views/Auth/AuthRegister.vue';
import AdminDashboard from '@/views/Admin/AdminDashboard.vue';
import CustomerDashboard from '@/views/Customer/CustomerDashboard.vue';
import ProfessionalDashboard from '@/views/Professional/ProfessionalDashboard.vue';

import ManageUser from '@/views/Admin/ManageUser.vue';
import ManageServices from '@/views/Admin/ManageServices.vue';
import ApproveProfessionals from '@/views/Admin/ApproveProfessionals.vue';
import AdminReports from '@/views/Admin/AdminReports.vue';

import AssignedRequests from '@/views/Professional/AssignedRequests.vue';

const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    component: AuthLogin,
    meta: {requiresGuest: true},
  },
  {
    path: '/register',
    component: AuthRegister,
    meta: {requiresGuest: true},
  },
  {
    path:'/admin',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: "admin" },
    children: [
      {
        path:'manage-users',
        component: ManageUser,
        meta: { requiresAuth: true, role: "admin" },
      },
      {
        path:'manage-services',
        component: ManageServices,
        meta: { requiresAuth: true, role: "admin" },
      },
      {
        path: 'approve-professionals',
        component: ApproveProfessionals,
        meta: { requiresAuth: true, role: "admin" },
      },
      {
        path: 'admin-reports',
        component: AdminReports,
        meta: { requiresAuth: true, role: "admin" },
      }
    ]
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
    children: [
      {
        path: 'assigned-requests',
        component: AssignedRequests,
        meta: { requiresAuth: true, role: "professional" },
      },
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth;
  const requiresGuest = to.meta.requiresGuest;
  // const userRole = localStorage.getItem('user_role');
  // const isAuthenticated = !!localStorage.getItem('access_token');
  const userRole = authState.userRole;
  const isAuthenticated = authState.isAuthenticated;
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
  } else if(requiresGuest){
    if(isAuthenticated){
      if (userRole == 'admin'){
        next('/admin');
      } else if(userRole == 'customer'){
        next('/customer');
      } else if(userRole == 'professional'){
        next('/professional');
      }
      else{
        next('/login');
      }
    }
  }
  else{
    next();
  }
});


export default router;
