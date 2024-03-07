<template>
  <div>
     <h2>Login</h2>
     <form @submit.prevent="loginUser">
       <label for="username">Username:</label>
       <input type="text" id="username" v-model="username" required>
       <label for="password">Password:</label>
       <input type="password" id="password" v-model="password" required>
       <button type="submit">Login</button>
       <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
     </form>
  </div>
 </template>
 
 <script>
 import axios from 'axios';
 
 export default {
  name: 'Login',
  data() {
     return {
       username: '',
       password: '',
       errorMessage: ''
     };
  },
  methods: {
     loginUser() {
       const path = 'http://127.0.0.1:5000/login_api';
       axios.post(path, {
           username: this.username,
           password: this.password
         })
         .then((res) => {
           localStorage.setItem('access_token', res.data.access_token);
           localStorage.setItem('role', res.data.role);
           localStorage.setItem('userName', res.data.user);

 
           if (res.data.role === 'user') {
             this.$router.push('/user-dashboard');
           } else if (res.data.role === 'librarian') {
             this.$router.push('/librarian-dashboard');
           } else if (res.data.role === 'admin') {
             this.$router.push('/admin-dashboard');
           }
           this.$emit('login-successful');

           this.username = '';
           this.password = '';
         })
         .catch((error) => {
      
           if (error.response && error.response.data && error.response.data.message) {
             this.errorMessage = error.response.data.message;
           } else {
             this.errorMessage = 'An unexpected error occurred. Please try again later.';
           }
         });
     },
  },
 };
 </script>
 
 <style scoped>
 .error {
  color: red;
 }
 </style>