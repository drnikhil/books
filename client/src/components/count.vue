<template>
    <div>
      <h2>User Count: {{ userCount }}</h2>
      <h2>Section Count: {{ sectionCount }}</h2>
      <h2>Book Count: {{ bookCount }}</h2>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {

    name : 'Count',

    data() {
      return {
        userCount: 0,
        sectionCount: 0,
        bookCount: 0
      };
    },
    mounted() {
      this.fetchCounts();
    },
    methods: {
      fetchCounts() {
        axios.get('http://127.0.0.1:5000/count')
          .then(response => {
            this.userCount = response.data.users;
            this.sectionCount = response.data.sections;
            this.bookCount = response.data.books;
          })
          .catch(error => console.error('Error fetching counts:', error));
      }
    }
  };
  </script>
  