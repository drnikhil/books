<template>
  <div class="section-list">
     <h2>Sections and Books</h2>
     <div v-for="section in sections" :key="section.id">
       <h3>{{ section.name }}</h3>
       <ul>
         <li v-for="book in section.books" :key="book.id">
           <span>{{ book.name }}</span>
           <button @click="deleteBook(book.id)" class="delete-button">Delete</button>
         </li>
       </ul>
     </div>
  </div>
 </template>
 
 <script>
 import axios from 'axios';
 
 export default {
  name: 'BookList',
  data() {
     return {
       sections: [],
     };
  },
  created() {
     this.fetchSections();
  },
  methods: {
     fetchSections() {
       axios.get('http://127.0.0.1:5000/get_sections_with_books')
         .then(response => {
           this.sections = response.data.sections;
         })
         .catch(error => {
           console.error('Error fetching sections:', error);
         });
     },
     deleteBook(bookId) {
       axios.delete(`http://127.0.0.1:5000/delete_book/${bookId}`)
         .then(response => {
           this.fetchSections(); // Refresh the sections and books after deletion
           console.log('Book deleted successfully.');
         })
         .catch(error => {
           console.error('Error deleting book:', error);
         });
     },
  },
 };
 </script>
 
 <style scoped>
 .section-list {
  background-color: #303030;
  color: white;
  padding: 20px;
 }
 
 .delete-button {
  background-color: red;
  color: white;
  padding: 5px 10px;
  border: none;
  cursor: pointer;
 }
 </style>