<template>

</template>

<script>
import axios from 'axios';

export default {
  name: 'BookDetails',

  data() {
    return {
      bookDetails: null
    };
  },

  created() {
    this.fetchBookDetails();
  },

  methods: {
    fetchBookDetails() {
      
      const rentalId = this.$route.params.rentalId;
      
      axios.get(`http://127.0.0.1:5000/bookdetails/${rentalId}`)
        .then(response => {
          this.bookDetails = response.data;
        })
        .catch(error => {
          console.error('Error fetching book details:', error);
        });
    }
  }
};
</script>

<style scoped>
  /* Your existing scoped styles */
</style>
