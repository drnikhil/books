import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/login.vue';
import Register from '../views/register.vue';
import Books from '../components/books.vue';
import Dashboard from '../views/Dashboard.vue'
import Navbar from '../components/navbar.vue'
import UserDashboard from '../views/UserDashboard.vue';
import LibrarianDashboard from '../views/LibrarianDashboard.vue';
import AdminDashboard from '../views/AdminDashboard.vue';

import BookList from '../components/booklist.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/books',
      name: 'books',
      component: Books
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/navbar',
      name: 'navbar',
      component: Navbar
    },
    {
      path: '/user-dashboard',
      name: 'userDashboard',
      component: UserDashboard,
      meta: { requiresAuth: true, role: 'user' }
     },
     {
      path: '/librarian-dashboard',
      name: 'librarianDashboard',
      component: LibrarianDashboard,
      meta: { requiresAuth: true, role: 'librarian' }
     },
     {
      path: '/admin-dashboard',
      name: 'adminDashboard',
      component: AdminDashboard,
      meta: { requiresAuth: true, role: 'admin' }
     },
     {
      path: '/booklist',
      name: 'booklist',
      component:BookList,

     }

  ]
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('access_token');
  const userRole = localStorage.getItem('role');
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else if (to.meta.role && to.meta.role !== userRole) {
    
    next('/' + userRole);
  } else {
    next();
  }
});

export default router;
