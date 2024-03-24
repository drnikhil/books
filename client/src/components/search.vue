<template>
  <div>    
    <nav class="navbar navbar-expand-lg navbar-chocolate bg-brown">
      <img src="../assets/ebook.png" alt="Logo" width="30" height="24" class="d-inline-block align-text-top">
      <router-link to="/login" class="navbar-brand">Bookworm</router-link>

      <form class="form-inline my-2 my-lg-0 ml-auto" @submit.prevent="performSearch">
        <div class="input-group">
          <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery">
          <div class="input-group-append">
            <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
          </div>
        </div>
      </form>
      <br>
      <div>
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Explore Premium</button>
      </div>
  
    </nav>

  
    <v-dialog v-model="modalVisible" max-width="600">
      <v-card>
        <v-card-title class="headline">Search Results</v-card-title>
        <v-card-text>
          <div v-if="searchResults.sections.length || searchResults.books.length">
            <ul>
              <li v-for="section in searchResults.sections" :key="section.id">SECTION:{{ section.name }}</li>
              <li v-for="book in searchResults.books" :key="book.id">BOOK :{{ book.name }}</li>
              <li v-for="book in searchResults.books" :key="book.id">AUTHOR:{{ book.authors }}</li>
            </ul>
          </div>
          <div v-else>
            <p>No results found</p>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="modalVisible = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

export default {
  name: 'Search',
  data() {
    return {
      searchQuery: '',
      searchResults: {
        sections: [],
        books: [],
        authors:[]

      },
      modalVisible: false  
    }
  },
  methods: {
    performSearch() {
      if (this.searchQuery.trim() === '') {
        console.log('Search query is empty');
        return;
      }
      const searchPath = 'http://localhost:5000/search?q=' + encodeURIComponent(this.searchQuery);
      axios.get(searchPath)
        .then((res) => {
          this.searchResults = res.data;
          this.modalVisible = true;  
          console.log(res.data);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }
}
</script>

<style scoped>
.btn {
  color: white;
  background-color: #6F4E37; 

}

.navbar {
  width: 100%; 
  position:fixed ; 
  top: 0; 
  z-index: 100; 
  left:0;

}
.form{
  position:fixed;
}
</style>
