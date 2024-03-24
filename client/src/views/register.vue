<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <h2>Register</h2>
        <form @submit.prevent="registerUser">
          <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" class="form-control" id="username" v-model="username" required>
          </div>
          <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" class="form-control" id="email" v-model="email" required>
          </div>
          <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" class="form-control" id="password" v-model="password" required>
          </div>
          <div class="form-group">
            <label for="confirm_password">Confirm Password:</label>
            <input type="password" class="form-control" id="confirm_password" v-model="confirmPassword" required>
          </div>
          <button type="submit" class="btn btn-primary">Register</button>
          <p v-if="errorMessage" class="error mt-3">{{ errorMessage }}</p>
          <p v-if="successMessage" class="success mt-3">{{ successMessage }}</p>
        </form>
        <div class="col-md-22">
            <a href="/login">Login here</a>
        </div>
      </div>

    </div>
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
      password: '',
      confirmPassword: '',
      errorMessage: '',
      successMessage: '',
    };
  },
  methods: {
    registerUser() {
      if (this.password !== this.confirmPassword) {
        this.errorMessage = "Passwords do not match";
        return;
      }

      const path = 'http://127.0.0.1:5000/register_api';
      axios.post(path, {
        username: this.username,
        email_address: this.email,
        password: this.password,
        confirm_password: this.confirmPassword 
      })
      .then((res) => {
        this.successMessage = "New user created successfully";
        setTimeout(() => {
          this.$router.push({ name: 'login' });
        }, 100);
      })
      .catch((error) => {
        this.errorMessage = error.response.data.message;
      });
    },
  },
};
</script>

<style scoped>
 div {
   max-width: 500px;
   margin: auto;
   background-color: #ffe4b5; /* Background color similar to old newspaper */
   padding: 5px;
   border-radius: 20px;
 }
.error {
  color: red;
}
.success {
  color: green;
}
</style>
