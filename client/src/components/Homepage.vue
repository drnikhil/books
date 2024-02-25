<template>
    <div class="home-page">
      <div class="navbar">
        <button @click="home">Home</button>
        <button @click="register">Register</button>
        <button @click="login">Login</button>
      </div>
  
      <div class="search-container">
        <h4>Welcome to Kitabwala</h4>
        <div class="search-box">
          <input type="text" v-model="searchQuery" placeholder="Search...">
          <button @click="search">Search</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        searchQuery: ''
      }
    },
    methods: {
      search() {
        // Implement search functionality
      },
      home() {
        // Handle navigation to home page
      },
      register() {
        // Handle navigation to register page
      },
      login() {
        // Handle navigation to login page
      }
    }
  }
  </script>
  
  <style>
  .landing-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }
  
  .navbar {
    width: 100%;
    background-color: #333;
    padding: 10px 0;
    text-align: center;
  }
  
  .navbar button {
    background-color: transparent;
    border: none;
    color: white;
    padding: 5px 10px;
    margin: 0 10px;
    cursor: pointer;
  }
  
  .search-container {
    text-align: center;
    margin-top: 20px;
  }
  
  .search-box {
    display: inline-block;
    margin-top: 20px;
  }
  
  .search-box input {
    padding: 8px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }
  
  .search-box button {
    padding: 8px 15px;
    background-color: blue;
    color: white;
    border: none;
    border-radius: 5px;
    margin-left: 5px;
    cursor: pointer;
  }
  </style>
  