<template>
  <div class="wrapper">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <img src="../assets/ebook.png" alt="Logo" width="30" height="24" class="d-inline-block align-text-top">
      <router-link to="/" class="navbar-brand">Bookworm</router-link>
      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link v-if="!loggedIn" to="/login" class="nav-link">Login</router-link>
            <router-link v-else to="#" class="nav-link" @click.prevent="logout">Logout</router-link>
          </li>
          <li class="nav-item">
            <router-link v-if="!loggedIn" to="/register" class="nav-link">Register</router-link>
          </li>
          <li class="nav-item" v-if="loggedIn">
            <span class="nav-link">{{ userName }}</span>
          </li>
        </ul>
        <form class="form-inline my-2 my-lg-0">
          <div class="input-group">
            <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery">
            <div class="input-group-append">
              <button class="btn btn-outline-success my-2 my-sm-0" type="submit" @click.prevent="performSearch">Search</button>
            </div>
            
          </div>
        </form>
      </div>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Dropdown link
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
          <a class="dropdown-item" href="#">Action</a>
          <a class="dropdown-item" href="#">Another action</a>
          <a class="dropdown-item" href="#">Something else here</a>
        </div>
      </li>
    </nav>
    
    <div v-if="searchResults.sections.length">
      <h3>Sections</h3>
      <ul>
        <li v-for="section in searchResults.sections" :key="section.id">{{ section.name }}</li>
      </ul>
    </div>
    <div v-if="searchResults.books.length">
      <h3>Books</h3>
      <ul>
        <li v-for="book in searchResults.books" :key="book.id">{{ book.title }}</li>
      </ul>
    </div>
    
  </div>
</template>

<script>
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

export default {
  name: 'Base',
  data() {
    return {
      loggedIn: false,
      userName: '',
      searchQuery: '',
      searchResults: {
        sections: [],
        books: []
      }
    }
  },
  methods: {
    logout() {
      this.loggedIn = false;
      this.userName = '';
    },
    performSearch() {
      if (this.searchQuery.trim() === '') {
        console.log('Search query is empty');
        return;
      }
      const searchPath = 'http://localhost:5000/search?q=' + encodeURIComponent(this.searchQuery);
      axios.get(searchPath)
        .then((res) => {
          this.searchResults = res.data;
          console.log(res.data);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }
}
</script>

<style>
.wrapper {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  flex-direction: column;
  min-height: 100vh;
  margin: 0 auto;
}

.footer {
  margin: auto;
  text-align: center;
  padding: 10px;
  background-color: black;
  color: white;
}

body {
  background-color: #4d3319;
  background-image: url('../assets/background.png');
  background-size: cover;
}
</style>
