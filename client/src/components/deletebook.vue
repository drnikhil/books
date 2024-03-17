<template>
    <div class="delete-book">
       <button @click="deleteBook" class="delete-button">Delete</button>
    </div>
   </template>
   
   <script>
   import axios from 'axios';
   
   export default {
    props: ['bookId'], // Accept the bookId as a prop
    data() {
       return {
         message: '',
       };
    },
    methods: {
       deleteBook() {
         axios.delete(`http://127.0.0.1:5000/delete_book/${this.bookId}`)
           .then(response => {
             this.$emit('bookDeleted'); // Emit an event to notify the parent component
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
   .delete-button {
    color: red;
    cursor: pointer;
   }
   </style>