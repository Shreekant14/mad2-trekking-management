import { createRouter, createWebHistory } from 'vue-router'

import { isAuthenticated, getCurrentUser } from '../services/auth'

import Login from '../views/auth/Login.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },

  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: {
      guest: true
    }
  },

  {
    path: '/admin',
    name: 'admin-dashboard',
    component: () => import('../views/admin/Dashboard.vue'),
    meta: {
      requiresAuth: true,
      role: 'ADMIN'
    }
  },

  {
    path: '/admin/treks',
    name: 'admin-treks',
    component: () => import('../views/admin/Treks.vue'),
    meta: {
      requiresAuth: true,
      role: 'ADMIN'
    }
  },

  {
    path: '/admin/users',
    name: 'admin-users',
    component: () => import('../views/admin/Users.vue'),
    meta: {
      requiresAuth: true,
      role: 'ADMIN'
    }
  },

  {
    path: '/admin/staff',
    name: 'admin-staff',
    component: () => import('../views/admin/Staff.vue'),
    meta: {
      requiresAuth: true,
      role: 'ADMIN'
    }
  },

  {
    path: '/admin/assignments',
    name: 'admin-assignments',
    component: () => import('../views/admin/Assignments.vue'),
    meta: {
      requiresAuth: true,
      role: 'ADMIN'
    }
  },

  {
    path: '/admin/bookings',
    name: 'admin-bookings',
    component: () => import('../views/admin/Bookings.vue'),
    meta: {
      requiresAuth: true,
      role: 'ADMIN'
    }
  },

  {
    path: '/staff',
    name: 'staff-dashboard',
    component: () => import('../views/staff/Dashboard.vue'),
    meta: {
      requiresAuth: true,
      role: 'STAFF'
    }
  },

  {
    path: '/staff/my-treks',
    name: 'staff-treks',
    component: () => import('../views/staff/MyTreks.vue'),
    meta: {
      requiresAuth: true,
      role: 'STAFF'
    }
  },

  {
    path: '/staff/participants',
    name: 'staff-participants',
    component: () => import('../views/staff/Participants.vue'),
    meta: {
      requiresAuth: true,
      role: 'STAFF'
    }
  },

  {
    path: '/staff/treks/:trekId/participants',
    name: 'staff-participants',
    component: () => import('../views/staff/Participants.vue')
  },

  {
    path: '/trekker',
    name: 'trekker-dashboard',
    component: () => import('../views/trekker/Dashboard.vue'),
    meta: {
      requiresAuth: true,
      role: 'TREKKER'
    }
  },

  {
    path: '/trekker/treks',
    name: 'trekker-treks',
    component: () => import('../views/trekker/Treks.vue'),
    meta: {
      requiresAuth: true,
      role: 'TREKKER'
    }
  },

  {
    path: '/trekker/bookings',
    name: 'trekker-bookings',
    component: () => import('../views/trekker/Bookings.vue'),
    meta: {
      requiresAuth: true,
      role: 'TREKKER'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const authenticated = isAuthenticated()
  const user = getCurrentUser()

  if (to.meta.requiresAuth && !authenticated) {
    return '/login'
  }

  if (to.meta.guest && authenticated && user) {
    if (user.role === 'ADMIN') return '/admin'
    if (user.role === 'STAFF') return '/staff'
    return '/trekker'
  }

  if (to.meta.role && user?.role !== to.meta.role) {
    if (user?.role === 'ADMIN') return '/admin'
    if (user?.role === 'STAFF') return '/staff'
    if (user?.role === 'TREKKER') return '/trekker'

    return '/login'
  }

  return true
})

export default router