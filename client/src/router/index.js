import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/login.vue'
import Admin from '../views/AdminDashboard.vue'
import User from '../views/UserDashboard.vue'
import Librarian from "../views/LibrarianDashboard.vue"
import Register from "../views/register.vue"



import Base from "../components/base.vue"
import BookList from "../components/booklist.vue"
import Search from '../components/search.vue'
import SectionList from '../components/SectionList.vue'
import Upload from '../components/upload.vue'
import AddBook from '../components/addbook.vue'
import DeleteBook from '../components/deletebook.vue'
import UpdateBook from "../components/updatebook.vue"
import LibraryPage from "../components/LibraryPage.vue"





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
    path: '/booklist',
    name: 'booklist',
    component: BookList
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
    path: '/addbook',
    name:'AddBook',
    component: AddBook
  },
  {
    path: '/deletebook',
    name:'DeleteBook',
    component: DeleteBook
  },
  {
    path:'/updatebook',
    name: 'UpdateBook',
    component: UpdateBook
  },
  {
    path:'/librarypage',
    name: 'LibraryPage',
    component: LibraryPage
  },

  ]
})

export default router
