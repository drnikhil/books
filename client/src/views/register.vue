\<template>
    <div>
      <h2>Register</h2>
      <form @submit.prevent="registerUser">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>

        <button type="submit">Register</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'Register',
    data() {
      return {
        username: '',
        email: '',
        password: ''
      };
    },
    methods: {
      registerUser() {
        const path = 'http://127.0.0.1:5000/register_api';
        axios.post(path, {
            username: this.username,
            email_address: this.email,
            password: this.password,

          
          })
          .then((res) => {
            console.log(res.data);
           
            this.$router.push({ name: 'login' });
          })
          .catch((error) => {
            this.errorMessage = error.response.data.message;
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
  