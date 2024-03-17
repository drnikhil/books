<template>
    <v-container>
      <!-- Display sections and books -->
      <v-row v-for="(section, index) in sections" :key="index">
        <v-col cols="12">
          <h2>{{ section.name }}</h2>
          <v-card v-for="(book, bookIndex) in section.books" :key="bookIndex" class="book-card">
            <v-card-title>{{ book.name }}</v-card-title>
            <v-card-text>
              <p>Authors: {{ book.authors }}</p>
              <p>Content: {{ book.content }}</p>
            </v-card-text>
            <v-card-actions>
              <v-btn @click="openUpdateBookModal(book)">Update Book</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
  
      <!-- Update Book Modal -->
      <v-dialog v-model="showUpdateBookModal" max-width="500">
        <template v-slot:activator="{ on }"></template>
        <v-card>
          <v-card-title>Update Book</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="updateBook">
              <v-text-field v-model="selectedBook.name" label="Book Name"></v-text-field>
              <v-text-field v-model="selectedBook.authors" label="Authors"></v-text-field>
              <v-textarea v-model="selectedBook.content" label="Content"></v-textarea>
              <v-btn type="submit">Update</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'UpdateBook',
  
    data() {
      return {
        sections: [],
        selectedBook: {},
        showUpdateBookModal: false
      };
    },
  
    mounted() {
      this.getSectionsWithBooks();
    },
  
    methods: {
      getSectionsWithBooks() {
        axios.get('http://127.0.0.1:5000/get_sections_with_books')
          .then(response => {
            this.sections = response.data.sections;
          })
          .catch(error => {
            console.error('Error fetching sections:', error);
          });
      },
  
      openUpdateBookModal(book) {
        this.selectedBook = { ...book };
        this.showUpdateBookModal = true;
      },
  
      updateBook() {
        const { id, name, content, authors } = this.selectedBook;
  
        axios.put(`http://127.0.0.1:5000/update_book/${id}`, {
          name,
          content,
          authors
        })
        .then(response => {
          console.log('Book updated successfully:', response.data);
          this.getSectionsWithBooks();
          this.showUpdateBookModal = false;
        })
        .catch(error => {
          console.error('Error updating book:', error);
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .book-card {
    margin-bottom: 10px;
  }
  </style>
  