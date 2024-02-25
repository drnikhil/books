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
          <li class="nav-item">
            <button class="nav-link" @click="openLoginModal">Login</button>
          </li>
          <li class="nav-item">
            <button class="nav-link" @click="openRegisterModal">Register</button>
          </li>
        </ul>
      </div>
    </div>

    <!-- Login Modal -->
    <div v-if="showLoginModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeLoginModal">&times;</span>
        <h2>Login Modal</h2>
        <button @click="loginAsUser" class="btn btn-primary">Login as User</button>
        <button @click="loginAsLibrarian" class="btn btn-secondary">Login as Librarian</button>
        <button @click="loginAsAdmin" class="btn btn-danger">Login as Admin</button>
        <p>Not a member? <router-link to="/register" class="register-link">Sign Up</router-link></p>
      </div>
    </div>

    <!-- Register Modal -->
    <div v-if="showRegisterModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeRegisterModal">&times;</span>
        <h2>Register Modal</h2>
        <!-- Add your register form here -->
        <Register @close="closeRegisterModal" />
      </div>
    </div>
  </nav>
</template>

<script>
import Register from './register.vue'; 
import User from './user.vue';
import LibrarianHomePage from './librarianhomepage.vue';
import Admin from './admin.vue';

export default {
  name: 'Navbar',
  components: {
    Register,
    User,
    LibrarianHomePage,
    Admin
  },
  data() {
    return {
      showLoginModal: false,
      showRegisterModal: false
    };
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
    loginAsUser() {
      // Redirect to User component or route
      this.$router.push('/user');
      this.closeLoginModal();
    },
    loginAsLibrarian() {
      // Redirect to LibrarianHomePage component or route
      this.$router.push('/librarian');
      this.closeLoginModal();
    },
    loginAsAdmin() {
      // Redirect to Admin component or route
      this.$router.push('/admin');
      this.closeLoginModal();
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
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999; /* Ensure modal is on top of other elements */
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

.register-link {
  color: blue;
  cursor: pointer;
}
</style>
