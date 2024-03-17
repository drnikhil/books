<template>
    <div class="section-list">
      <h2>Sections and Books</h2>
      <div v-for="section in sections" :key="section.id">
        <h3>{{ section.name }}</h3>
        <table class="books-table">
          <thead>
            <tr>
              <th>Book Name</th>
              <th>Update</th>
              <th>Delete</th>
              <th>Choose File</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in section.books" :key="book.id">
              <td>{{ book.name }}</td>
              <td>
                <button @click="openUpdateBookModal(book)" class="action-button">Update</button>
              </td>
              <td>
                <button @click="deleteBook(book.id)" class="action-button">Delete</button>
              </td>
              <td>
                <button @click="chooseFile(book.id)" class="action-button">Choose File</button>
              </td>
              
            </tr>
          </tbody>
        </table>
        <div class="action-buttons">
          <button @click="showAddBookModal = true" class="action-button">Add Book</button>
          <Upload @fileUploaded="fetchSections" />
        </div>
      </div>
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
    </div>
  </template>
  
  
  <script>
  import axios from 'axios';
  import Upload from '@/components/Upload.vue';
  
  export default {
    name: 'LibraryPage',

    components: {
    Upload 
    },
    data() {
       return {
         sections: [],
         newBook: {
           name: '',
           content: '',
           authors: '',
           section_id: null,
         },
         selectedBook: {},
         showAddBookModal: false,
         showUpdateBookModal: false,
         // Add other modal states as needed
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
       addNewBook() {
         axios.post('http://127.0.0.1:5000/add_book', this.newBook)
           .then((res) => {
             console.log('Book added successfully:', res.data);
             this.fetchSections(); // Refresh the sections and books after adding new book
           })
           .catch((error) => {
             console.error('Error adding book:', error);
           })
           .finally(() => {
             this.showAddBookModal = false; // Close the modal after submitting the form
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
           this.fetchSections();
           this.showUpdateBookModal = false;
         })
         .catch(error => {
           console.error('Error updating book:', error);
         });
       }
       // Implement other methods for section and book actions as needed
    },
  };
  </script>
  
  <style scoped>
  .section-list {
    background-color: #303030;
    color: white;
    padding: 20px;
  }
  
  .action-buttons {
    margin-top: 10px;
  }
  
  .action-button {
    margin-right: 10px;
  }
  </style>