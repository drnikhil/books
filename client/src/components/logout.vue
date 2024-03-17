<template>
    <v-btn color="red darken-1" @click="logout">Logout</v-btn>
  </template>
  
  <script>
  import router from '../router/index.js'; 
  
  export default {

    name: "Logout",
    
    methods: {
      logout() {
        
        localStorage.removeItem('token');
  
        
        router.push('/login');
      },
    },
  };
  </script>
  
  <style>
 
  </style>
  