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
          // Store the access token and role in local storage
          localStorage.setItem('access_token', res.data.access_token);
          localStorage.setItem('role', res.data.role);
          
          // Redirect to the appropriate dashboard based on the role
          switch (res.data.role) {
            case 'admin':
              this.$router.push('/admin');
              break;
            case 'librarian':
              this.$router.push('/librarian');
              break;
            case 'user':
              this.$router.push('/user');
              break;
            default:
              // Redirect to a default route if the role is not recognized
              this.$router.push('/');
              break;
          }
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
