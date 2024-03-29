import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/login.vue'
import Admin from '../views/AdminDashboard.vue'
import User from '../views/UserDashboard.vue'
import Librarian from "../views/LibrarianDashboard.vue"
import Register from "../views/register.vue"



import Base from "../components/base.vue"
import Search from '../components/search.vue'
import SectionList from '../components/SectionList.vue'
import Upload from '../components/upload.vue'


import LibraryPage from "../components/LibraryPage.vue"
import Count from "../components/count.vue"
import Rentals from "../components/rentals.vue"
import Read from "../components/read.vue"
import BookDetails from "../components/bookdetails.vue"




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/search',
      name: 'Search',
      component: Search

    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {path: '/admin',
    name: 'Admin',
    component: Admin
  },
  {
    path:'/lib',
    name:'librarian',
    component: Librarian
  },
  {
    path:'/user',
    name: 'user',
    component: User
  },

  {
    path: '/register',
    name: 'register',
    component: Register
  },
  {
    path: '/base',
    name: 'base',
    component: Base
  },

  {
    path: '/sections',
    name: SectionList,
    component: SectionList
  },
  {
    path: '/upload',
    name:'Upload',
    component: Upload
  },



  {
    path:'/librarypage',
    name: 'LibraryPage',
    component: LibraryPage
  },
  {
    path:'/count',
    name: 'Count',
    component: Count
  },
  {
    path: '/logout',
    name: 'Logout',
    component: Count
  },

  {
    path:'/rentals',
    name: 'Rentals',
    component: Rentals
  },
  {
    path:'/readbook',
    name:'Read',
    component: Read
  },
  {
    path: '/bookdetails/',
    name: 'BookDetails',
    component: BookDetails
   }


  ]
})

export default router
