<template>
  <v-container>
    <v-btn @click="showAddBookModal = true">Add New Book</v-btn>

    <!-- Add Book Modal -->
    <v-dialog v-model="showAddBookModal" max-width="500">
      <template v-slot:activator="{ on }"></template>
      <v-card>
        <v-card-title>Add New Book</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="addNewBook">
            <v-text-field v-model="newBook.section_id" label="Section ID"></v-text-field>
            <v-text-field v-model="newBook.name" label="Book Name"></v-text-field>
            <v-text-field v-model="newBook.authors" label="Authors"></v-text-field>
            <v-textarea v-model="newBook.content" label="Content"></v-textarea>
            <v-btn type="submit">Add Book</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AddBook',

  data() {
    return {
      newBook: {
        name: '',
        content: '',
        authors: '',
        section_id: null,
      },
      showAddBookModal: false
    };
  },

  methods: {
    addNewBook() {
      axios.post('http://127.0.0.1:5000/add_book', this.newBook)
        .then((res) => {
          console.log('Book added successfully:', res.data);
          // Optionally, you can emit an event or perform any other action upon successful addition of the book
        })
        .catch((error) => {
          console.error('Error adding book:', error);
        })
        .finally(() => {
          this.showAddBookModal = false; // Close the modal after submitting the form
        });
    }
  }
};
</script>

<style scoped>
/* Add your scoped styles here */
</style>
