import { createRouter, createWebHistory } from 'vue-router';
import { authState } from '@/services/auth';
import AuthLogin from '@/views/Auth/AuthLogin.vue';
import AuthRegister from '@/views/Auth/AuthRegister.vue';
import AdminDashboard from '@/views/Admin/AdminDashboard.vue';
import CustomerDashboard from '@/views/Customer/CustomerDashboard.vue';
import ProfessionalDashboard from '@/views/Professional/ProfessionalDashboard.vue';
import AdminSummary from '@/views/Admin/AdminSummary.vue';

import ManageUser from '@/views/Admin/ManageUser.vue';
import ManageServices from '@/views/Admin/ManageServices.vue';
import ApproveProfessionals from '@/views/Admin/ApproveProfessionals.vue';
import AdminReports from '@/views/Admin/AdminReports.vue';
import EditService from '@/views/Admin/EditService.vue';

import AssignedRequests from '@/views/Professional/AssignedRequests.vue';

import AvailableServices from '@/views/Customer/AvailableServices.vue';
import RequestService from '@/views/Customer/RequestService.vue';
import CustomerServiceRequests from '@/views/Customer/CustomerServiceRequests.vue';
import ProvideReview from '@/views/Customer/ProvideReview.vue';
import CustomerProfile from '@/views/Customer/CustomerProfile.vue';
import ProfessionalProfile from '@/views/Professional/ProfessionalProfile.vue';
import ProfessionalPendingApproval from '@/views/Professional/ProfessionalPendingApproval.vue';
import AdminSearch from '@/views/Admin/AdminSearch.vue';
import ProfessionalSearch from '@/views/Professional/ProfessionalSearch.vue';
import ProfessionalSummary from '@/views/Professional/ProfessionalSummary.vue';
import CustomerSummary from '@/views/Customer/CustomerSummary.vue';

import SearchResults from '@/views/SearchResults.vue';

const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    component: AuthLogin,
    meta: { requiresGuest: true },
  },
  {
    path: '/register',
    component: AuthRegister,
    meta: { requiresGuest: true },
  },
  {
    path: '/admin/search',
    name: 'AdminSearch',
    component: AdminSearch,
    meta: { requiresAuth: true, role: 'admin' }, 
  }, 
  {
    path: '/professional/search',
    name: 'ProfessionalSearch',
    component: ProfessionalSearch,
    meta: { requiresAuth: true, role: 'professional' }, 
  }, 
  {
    path: '/customer/search',
    name: 'CustomerSearch',
    component: () => import('@/views/Customer/CustomerSearch.vue'),
    meta: { requiresAuth: true, role: 'customer' },
  },
  {
    path: '/customer/search-results',
    name: 'CustomerSearchResults',
    component: () => import('@/views/Customer/CustomerSearchResults.vue'),
    meta: { requiresAuth: true, role: 'customer' },
  },
  {
    path: '/admin/search-results',
    name: 'AdminSearchResults',
    component: () => import('@/views/Admin/AdminSearchResults.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },  
  {
    path: '/professional/search-results',
    name: 'ProfessionalSearchResults',
    component: () => import('@/views/Professional/ProfessionalSearchResults.vue'),
    meta: { requiresAuth: true, role: 'professional' }
  },
  {
    path: '/admin/admin-summary',
    name: 'AdminSummary',
    component: AdminSummary
  },  
  {
    path: '/professional/summary',
    name: 'ProfessionalSummary',
    component: ProfessionalSummary,
    meta: { requiresAuth: true, role: 'professional' }
  },  
  {
    path: '/customer/summary',
    name: 'CustomerSummary',
    component: CustomerSummary,
    meta: { requiresAuth: true, role: 'customer' }
  },  
  
  {
    path: '/admin',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      // { path: 'admin-summary', component: AdminSummary },
      {
        path: 'manage-users',
        component: ManageUser,
        meta: { requiresAuth: true, role: 'admin' },
      },
      {
        path: 'manage-services',
        name: 'ManageServices',
        component: ManageServices,
        meta: { requiresAuth: true, role: 'admin' },
      },
      {
        path: 'approve-professionals',
        component: ApproveProfessionals,
        meta: { requiresAuth: true, role: 'admin' },
      },
      {
        path: 'admin-reports',
        component: AdminReports,
        meta: { requiresAuth: true, role: 'admin' },
      },
      {
        path: '/admin/service/:id/edit',
        name: 'EditService',
        component: EditService,
        meta: { requiresAuth: true, role: 'admin' },
      },
    ],
  },
  {
    path: '/customer',
    component: CustomerDashboard,
    meta: { requiresAuth: true, role: 'customer' },
    children: [
      {
        path: 'services',
        name: 'AvailableServices',
        component: AvailableServices,
      },
      // {
      //   path: 'services/:serviceId/request',
      //   name: 'RequestService',
      //   component: RequestService,
      //   props: true,
      // },
      {
        path: '/customer/request-service/:serviceId/:packageId?',
        name: 'RequestService',
        component: RequestService,
        props: true,
      },
      {
        path: 'service_requests',
        name: 'CustomerServiceRequests',
        component: CustomerServiceRequests,
      },
      {
        path: 'service_requests/:requestId/review',
        name: 'ProvideReview',
        component: ProvideReview,
        props: true,
      },
    ],
  },
  {
    path: '/customer/profile',
    name: 'CustomerProfile',
    component: CustomerProfile,
    meta: { requiresAuth: true, role: 'customer' },
  },
  {
    path: '/professional/profile',
    name: 'ProfessionalProfile',
    component: ProfessionalProfile,
    meta: { requiresAuth: true, role: 'professional' },
  },
  {
    path: '/professional/pending-approval',
    name: 'ProfessionalPendingApproval',
    component: ProfessionalPendingApproval,
    meta: { requiresAuth: true, role: 'professional' },
  },
  {
    path: '/search-results/:role',
    name: 'SearchResults',
    component: SearchResults,
    props: (route) => ({
      role: route.params.role,
      results: route.query.results ? JSON.parse(route.query.results) : []
    }),
    meta: { requiresAuth: true },
  },
  {
    path: '/professional',
    component: ProfessionalDashboard,
    meta: { requiresAuth: true, role: 'professional' },
    children: [
      {
        path: 'assigned-requests',
        component: AssignedRequests,
        meta: { requiresAuth: true, role: 'professional' },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth;
  const requiresGuest = to.meta.requiresGuest;
  const userRole = authState.userRole;
  const isAuthenticated = authState.isAuthenticated;
  const profileComplete = authState.profileComplete;

  console.log('Navigating to:', to.path);
  console.log('Requires Auth:', requiresAuth);
  console.log('User Role:', userRole);
  console.log('Is Authenticated:', isAuthenticated);
  console.log('Profile Complete:', profileComplete);

  if (requiresAuth) {
    if (isAuthenticated) {
      if (to.meta.role === userRole) {
        if (userRole === 'customer' && !profileComplete && to.path !== '/customer/profile') {
          return next('/customer/profile');
        }
        if (userRole === 'professional' && !profileComplete && to.path !== '/professional/profile') {
          return next('/professional/profile');
        }
        return next();
      } else {
        return next('/login');
      }
    } else {
      return next('/login');
    }
  } else if (requiresGuest) {
    if (isAuthenticated) {
      if (userRole === 'admin') {
        return next('/admin');
      } else if (userRole === 'customer') {
        if (!profileComplete) {
          return next('/customer/profile');
        } else {
          return next('/customer');
        }
      } else if (userRole === 'professional') {
        if (!profileComplete) {
          return next('/professional/profile');
        } else {
          return next('/professional');
        }
      } else {
        return next('/login');
      }
    } else {
      return next();
    }
  } else {
    return next();
  }
});

export default router;
