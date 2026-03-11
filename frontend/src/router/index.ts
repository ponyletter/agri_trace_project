import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/dashboard',
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/login/LoginView.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/trace/:code',
      name: 'TracePublic',
      component: () => import('../views/trace/TracePublicView.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/batches',
      name: 'BatchList',
      component: () => import('../views/batch/BatchListView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/trace-records',
      name: 'TraceRecords',
      component: () => import('../views/trace/TraceRecordsView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/admin/users',
      name: 'AdminUsers',
      component: () => import('../views/admin/UserManageView.vue'),
      meta: { requiresAuth: true, role: 'admin' },
    },
  ],
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
