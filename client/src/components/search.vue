<template>
  <div>
     <h1>Search</h1>
     <div class="search-container">
       <input v-model="searchQuery" type="text" placeholder="Search..." class="search-input">
       <button class="search-button" @click="performSearch">Search</button>
     </div>
     <div v-if="searchResults.sections.length || searchResults.books.length">
       <h2>Search Results</h2>
       <div v-if="searchResults.sections.length">
         <h3>Sections</h3>
         <ul>
           <li v-for="section in searchResults.sections" :key="section.id">
             {{ section.name }}
           </li>
         </ul>
       </div>
       <div v-if="searchResults.books.length">
         <h3>Books</h3>
         <ul>
           <li v-for="book in searchResults.books" :key="book.id">
             {{ book.title }}
           </li>
         </ul>
       </div>
 
     </div>
  </div>
</template>
   
   <script>
   import axios from 'axios';
   
   export default {
    name: 'Search',
    data() {
       return {
         searchQuery: '',
         searchResults: {
           sections: [],
           books: [],
     
         }
        
       };
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
             console.log(this.searchResults);
           })
           .catch((error) => {
             console.error(error);
           });
       }
    }
   };
   </script>
   
   <style scoped>
   .search-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 1em;
   }
   
   .search-input {
    margin-right: 10px;
   }
   
   .search-button {
    background-color: #007bff;
    color: #fff;
    border: none;
    padding: 8px 16px;
    border-radius: 5px;
    cursor: pointer;
   }
   </style>
