<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Books</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" @click="showAddBookForm = true">Add Book</button>
        <br><br>
        <form v-if="showAddBookForm" @submit.prevent="handleAddBook">
          <div class="mb-3">
            <label for="bookTitle" class="form-label">Title:</label>
            <input type="text" class="form-control" id="bookTitle" v-model="newBook.title" placeholder="Enter title">
          </div>
          <div class="mb-3">
            <label for="bookAuthor" class="form-label">Author:</label>
            <input type="text" class="form-control" id="bookAuthor" v-model="newBook.author" placeholder="Enter author">
          </div>
          <div class="mb-3">
            <label for="bookSection" class="form-label">Section:</label>
            <input type="text" class="form-control" id="bookSection" v-model="newBook.section" placeholder="Enter section">
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
          <button type="button" class="btn btn-secondary" @click="showAddBookForm = false">Cancel</button>
        </form>
      
  
      <table class="table table-hover">
        <thead>
          <tr>
            <th scope="col">Title</th>
            <th scope="col">Author</th>
            <th scope="col">Section</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(book, index) in books" :key="index">
            <td>{{ book.name }}</td>
            <td>{{ book.authors }}</td>
            <td>{{ book.section_name }}</td>
            <td>
              <div class="btn-group" role="group">
                <button type="button" class="btn btn-warning btn-sm">Update</button>
                <button type="button" class="btn btn-danger btn-sm">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
      </div>
 </div>
</template>
        

<script>
import axios from 'axios';


export default {
  name: 'BooksList',
  data() {
    return {
      books: [],
      showAddBookForm: false, 
      newBook: {
        title: '',
        author: '',
        section: '',
      },
    };
  },
  methods: {
    getBooks() {
      const path = 'http://127.0.0.1:5000/getbooks';
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
        })
        .catch((error) => {
          console.error('Error fetching books:', error);
        });
    },
    handleAddBook() {
      const path = 'http://127.0.0.1:5000/add_book';
      axios.post(path, this.newBook)
        .then(() => {
          this.getBooks();
          this.showAddBookForm = false; 
        })
        .catch((error) => {
          console.error('Error adding book:', error);
        });
    },
  },
  created() {
    this.getBooks();
  },
};
</script>