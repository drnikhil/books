import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import Login from '../components/login.vue';
import Register from '../components/register.vue';
import Books from '../components/books.vue';
import Librarian from '../components/LibrarianDashboard.vue';
import Admin from '../components/AdminDashboard.vue'
import User from '../components/UserDashboard.vue'
import Navbar from '../components/navbar.vue'

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
      path: '/librarian',
      name: 'librarian',
      component: Librarian,
      meta: { requiresAuth: true, role: 'librarian' }
    },
    {
      path: '/admin',
      name: 'admin',
      component: Admin,
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/user',
      name: 'user',
      component: User,
      meta: { requiresAuth: true, role: 'user' } 
    },
    {
      path: '/navbar',
      name: 'navbar',
      component: Navbar
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
