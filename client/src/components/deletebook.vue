<template>
    <div class="delete-book">
       <h2>Delete Book</h2>
       <p>Enter the ID of the book you want to delete:</p>
       <input type="number" v-model="bookId" placeholder="Book ID" class="book-id-input">
       <button @click="deleteBook" class="delete-button">Delete Book</button>
       <p v-if="message">{{ message }}</p>
    </div>
   </template>
   
   <script>
   import axios from 'axios';
   
   export default {

    name : 'DeleteBook',

    data() {
       return {
         bookId: null,
         message: '',
       };
    },
    methods: {
       deleteBook() {
         if (!this.bookId) {
           this.message = 'Please enter a book ID.';
           return;
         }
   
         axios.delete(`http://127.0.0.1:5000/delete_book/${this.bookId}`)
           .then(response => {
             this.message = 'Book deleted successfully.';
             this.bookId = null; // Clear the input field
           })
           .catch(error => {
             this.message = 'Error deleting book.';
             console.error('Error deleting book:', error);
           });
       },
    },
   };
   </script>
   
   <style scoped>
   .delete-book {
    background-color: #303030;
    color: white;
    padding: 20px;
   }
   
   .book-id-input {
    margin-bottom: 10px;
    padding: 5px;
    width: 100%;
   }
   
   .delete-button {
    background-color: red;
    color: white;
    padding: 5px 10px;
    border: none;
    cursor: pointer;
   }
   </style>