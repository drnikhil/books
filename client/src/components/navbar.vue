<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <router-link to="/" class="navbar-brand">Kitabwala</router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            
            <button class="nav-link" @click="openLoginModal">Login</button>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <button class="nav-link" @click="openRegisterModal">Register</button>
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <span class="nav-link">{{ userName }}</span>
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <button class="nav-link" @click="logout">Logout</button>
          </li>
        </ul>
      </div>
    </div>

    <!-- Login Modal -->
    <div v-if="showLoginModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeLoginModal">&times;</span>
        <h2>Login</h2>
        <form @submit.prevent="loginUser" class="login-form">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="username" required>
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" required>
          <button type="submit" class="btn btn-primary">Login</button>
          <p class="error" v-if="errorMessage">{{ errorMessage }}</p>
        </form>
        <p class="register-link">Not a member? <router-link to="/register">Sign Up</router-link></p>
      </div>
    </div>

    <!-- Register Modal -->
    <div v-if="showRegisterModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeRegisterModal">&times;</span>
        <h2>Register</h2>
        <!-- Your registration component goes here -->
        <Register @close="closeRegisterModal" />
      </div>
    </div>
  </nav>
</template>

<script>
import axios from 'axios';
import Register from './register.vue';
import Login from './login.vue';

export default {
  name: 'Navbar',
  components: {
    Register,
    Login
  },
  data() {
    return {
      showLoginModal: false,
      showRegisterModal: false,
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('access_token');
    },
    userName() {
      return localStorage.getItem('username') || 'Guest';
    }
  },
  methods: {
    openLoginModal() {
      this.showLoginModal = true;
    },
    closeLoginModal() {
      this.showLoginModal = false;
    },
    openRegisterModal() {
      this.showRegisterModal = true;
    },
    closeRegisterModal() {
      this.showRegisterModal = false;
    },
    logout() {
      axios.delete('/logout', userData)
        .then(() => {
          localStorage.removeItem('access_token');
          localStorage.removeItem('username');
        });
    },
    loginUser() {
      const userData = {
        username: this.username,
        password: this.password
      };

      axios.post('/login_api', userData)
        .then(response => {
          const { access_token, username } = response.data;

          localStorage.setItem('access_token', access_token);
          localStorage.setItem('username', username);

          this.$router.push('/dashboard');

          this.closeLoginModal();
        })
        .catch(error => {
          console.error('Login failed:', error);

          this.errorMessage = 'Invalid username or password. Please try again.';
        });
    }
  }
};
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.navbar-toggler {
  color: #fff;
  border: none;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999; 
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
}

.login-form label {
  display: block;
  margin-bottom: 5px;
}

.login-form input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.register-link {
  color: blue;
  cursor: pointer;
}

.btn {
  padding: 8px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: #fff;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.error {
  color: red;
}
</style>
