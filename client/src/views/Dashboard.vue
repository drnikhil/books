<template>
    <div>
      <h1>Welcome to the Dashboard!</h1>
      <template v-if="userRole === 'admin'">
        <AdminDashboard />
      </template>
      <template v-else-if="userRole === 'librarian'">
        <LibrarianDashboard />
      </template>
      <template v-else>
        <UserDashboard />
      </template>
    </div>
  </template>
  
  <script>
  import { computed } from 'vue';
  import Admin from '../AdminDashboard.vue';
  import Librarian from './LibrarianDashboard.vue';
  import User from './UserDashboard.vue';
  
  export default {
    name: 'Dashboard',
    components: {
      Admin,
      Librarian,
      User
    },
    setup() {
      const userRole = computed(() => {
        return localStorage.getItem('role');
      });
  
      return { userRole };
    }
  };
  </script>
  