<template>
  <div class="section-list">
    <h2>Sections and Books</h2>
    <div v-for="section in sections" :key="section.id">
      <h3>{{ section.name }}</h3>
      <ul>
        <li v-for="book in section.books" :key="book.id">
          <span>{{ book.name }}</span>
          <button @click="deleteBook(book.id)" class="action-button">Delete</button>
          <button @click="openUpdateBookModal(book)" class="action-button">Update</button>
          
          
          <Upload :bookId="book.id" @fileUploaded="uploadFileAndAddBook(book.id)" />
        </li>
      </ul>
      <div class="action-buttons">
        <!-- Move the "Add Book" button inside the loop to be next to each section -->
        <button @click="showAddBookModal = true" class="action-button">Add Book</button>
      </div>
    </div>

    <!-- Add Book Modal -->
    <v-dialog v-model="showAddBookModal" max-width="500">
      <template v-slot:activator="{ on }"></template>
      <v-card>
        <v-card-title>Add New Book</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="addNewBook">
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
        authors: ''
      },
      selectedBook: {},
      showAddBookModal: false,
      showUpdateBookModal: false
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
          this.showAddBookModal = false; // Close the modal after submitting the form
        })
        .catch((error) => {
          console.error('Error adding book:', error);
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
    },
    uploadFileAndAddBook(file_path) {
      this.newBook.file_path = file_path;
      this.addNewBook();
    }
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
