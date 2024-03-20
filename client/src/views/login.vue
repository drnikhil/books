<template>
  <div>
     <h2 style="font-family: 'Times New Roman', Times, serif; font-size: 24px; text-align: center;">Login</h2>
     <form @submit.prevent="loginUser" style="background-color: #f0f0f0; padding: 20px; border-radius: 10px;">
       <label for="username" style="font-family: 'Times New Roman', Times, serif; font-size: 18px;">Username:</label>
       <input type="text" id="username" v-model="username" required style="font-family: 'Courier New', Courier, monospace; font-size: 16px; width: 100%; padding: 12px 20px; margin: 8px 0; border: 1px solid #000;">
       <label for="password" style="font-family: 'Times New Roman', Times, serif; font-size: 18px;">Password:</label>
       <input type="password" id="password" v-model="password" required style="font-family: 'Courier New', Courier, monospace; font-size: 16px; width: 100%; padding: 12px 20px; margin: 8px 0; border: 1px solid #000;">
       <button type="submit" style="font-family: 'Courier New', Courier, monospace; font-size: 16px; background-color: #4CAF50; color: white; padding: 14px 20px; margin: 8px 0; border: none; cursor: pointer; border-radius: 5px; width: 100%;">Login</button>
       <p v-if="errorMessage" class="error" style="font-family: 'Courier New', Courier, monospace; font-size: 16px; color: red; margin-top: 10px;">{{ errorMessage }}</p>
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
           localStorage.setItem('username', res.data.username);
           localStorage.setItem('user_id', res.data.user_id); // Set the user_id

           if (res.data.role === 'user') {
             this.$router.push('/user');
           } else if (res.data.role === 'librarian') {
             this.$router.push('/lib');
           } else if (res.data.role === 'admin') {
             this.$router.push('/admin');
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
 div {
   max-width: 300px;
   margin: auto;
   background-color: #ffe4b5; /* Background color similar to old newspaper */
   padding: 20px;
   border-radius: 10px;
 }

 input[type="text"],
 input[type="password"] {
   width: 100%;
   padding: 12px 20px;
   margin: 8px 0;
   display: inline-block;
   border: 1px solid #000;
   box-sizing: border-box;
   background-color: #f0f0f0; /* Input background color */
   color: #000; /* Input text color */
   font-family: 'Courier New', Courier, monospace;
   font-size: 16px;
 }

 /* Form submit button */
 button[type="submit"] {
   background-color: #4CAF50; /* Green background color */
   color: white; /* Button text color */
   padding: 14px 20px;
   margin: 8px 0;
   border: none;
   cursor: pointer;
   width: 100%;
   border-radius: 5px;
   font-family: 'Courier New', Courier, monospace;
   font-size: 16px;
 }

 /* Error message */
 .error {
   color: red; /* Keep error message color as red */
   font-family: 'Courier New', Courier, monospace;
   font-size: 16px;
   margin-top: 10px;
 }
 
 </style>
