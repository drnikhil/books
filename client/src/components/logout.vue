<template>
  <v-btn color="red darken-1" @click="logout">Logout</v-btn>
</template>

<script>
import axios from 'axios';
import router from '../router/index.js';

export default {
  name: "Logout",
  methods: {
    logout() {

      localStorage.clear()
      this.$router.push({path:'/login'})
      
      }
    }
  }


</script>

<style>
</style>
