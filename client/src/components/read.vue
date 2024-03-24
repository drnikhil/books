<template>
    <div>
      <h2>{{ bookName }}</h2>
      <button @click="readBook">Read Book</button>
      <div v-if="bookContent">
        <iframe :src="bookContent" width="100%" height="600px"></iframe>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {

    name: 'Read', 

    data() {
      return {
        bookName: '',
        bookId: 0,
        bookContent: '',
      };
    },
    methods: {
      readBook() {
        
        axios.get(`http://127.0.0.1:5000/read_book/${rental_id}`)
          .then(response => {
            this.bookContent = response.data;
          })
          .catch(error => {
            console.error('Error reading book:', error);
          });
      }
    }
  };
  </script>
  
  <style scoped>
  
  </style>
  