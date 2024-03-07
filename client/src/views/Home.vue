<template>
  <div class="home">
    <Navbar/>

    <h1>Welcome to Kitabwala</h1>
    <p>Explore our large collection of books</p>

    <!-- Search Bar -->
    <input type="text" v-model="searchQuery" placeholder="Search books..." class="search-bar">
    <button @click="searchBooks" class="btn">Search</button>
    
    <!-- Display Books in Tabular Format -->
    <div v-if="books.length === 0">No books found.</div>
    <div v-else>
      <table class="book-table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in filteredBooks" :key="book.id">
            <td>{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.description }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from './navbar.vue';


export default {
  name: 'Home',
  components: {
    Navbar,

  },
  data() {
    return {
      books: [], 
      searchQuery: '', 
    };
  },
  methods: {
    fetchBooks() {
      const path = 'http://127.0.0.1:5000/getbooks';
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
        })
        .catch((error) => {
          console.error('Error fetching books:', error);
        });
    },
    searchBooks() {
      // Perform search logic based on searchQuery
      // For simplicity, let's assume we fetch all books again and filter them
      this.fetchBooks();
    }
  },
  created() {
    // Fetch books when the component is created
    this.fetchBooks();
  },
  computed: {
    filteredBooks() {
      // Filter books based on the search query
      return this.books.filter(book =>
        book.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        book.author.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        book.description.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  }
};
</script>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}

.btn {
  margin-left: 10px;
  padding: 8px 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn:hover {
  background-color: #0056b3;
}

.search-bar {
  margin-top: 20px;
  padding: 8px;
  width: 300px;
}

.book-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.book-table th, .book-table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.book-table th {
  background-color: #f2f2f2;
}

.book-table td {
  text-align: left;
}

</style>
