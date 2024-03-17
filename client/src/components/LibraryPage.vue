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
            <th>File Path</th> <!-- Display File Path -->
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
            <td>{{ book.file_path }}</td> <!-- Display File Path -->
          </tr>
        </tbody>
      </table>
      <div class="action-buttons">
        <Upload v-if="selectedBookId" :bookId="selectedBookId" @fileUploaded="fetchSections" />
        <button @click="showAddBookModal = true" class="action-button">Add Book</button>
      </div>
    </div>
    
    <!-- Add Book Modal -->
    <!-- Update Book Modal -->
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
      selectedBookId: null,
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
    chooseFile(bookId) {
      this.selectedBookId = bookId; 
      console.log('Selected book ID:', this.selectedBookId);
    },
    addNewBook() {
      axios.post('http://127.0.0.1:5000/add_book', this.newBook)
        .then((res) => {
          console.log('Book added successfully:', res.data);
          this.fetchSections(); 
        })
        .catch((error) => {
          console.error('Error adding book:', error);
        })
        .finally(() => {
          this.showAddBookModal = false; 
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
  }
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
