<template>
  <div>
    <div>Welcome Bookworm {{ username }}</div>
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>Section</th>
            <th>Books</th>
            <th>Authors</th>
            <th>Content</th>
            
            <th>Ratings</th>
            <th>Comments</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="section in sections" :key="section.id">
            <td>{{ section.name }}</td>
            <td>
              <ul v-if="section.books && section.books.length">
                <li v-for="book in section.books" :key="book.id">{{ book.name }}</li>
              </ul>
              <span v-else>No books available</span>
            </td>
            <td>
              <ul v-if="section.books && section.books.length">
                <li v-for="book in section.books" :key="book.id">{{ book.authors }}</li>
              </ul>
              <span v-else>N/A</span>
            </td>
            <td>
              <ul v-if="section.books && section.books.length">
                <li v-for="book in section.books" :key="book.id">{{ book.content }}</li>
              </ul>
              <span v-else>N/A</span>
            </td>

            <td>
              <ul v-if="section.books && section.books.length">
                <li v-for="book in section.books" :key="book.id">{{ book.rating }}</li>
              </ul>
              <span v-else>N/A</span>
            </td>
            <td>
              <ul v-if="section.books && section.books.length">
                <li v-for="book in section.books" :key="book.id">{{ book.comments }}</li>
              </ul>
              <span v-else>N/A</span>
            </td>
            <td>
              <button @click="requestBook(section.id)">Request Book</button>
              <button @click="readBook(section.id)" :disabled="!section.approved">Read</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Base from '@/components/Base.vue';

export default {
  name: 'User',
  components: {
    Base
  },
  data() {
    return {
      sections: [],
      username: localStorage.getItem('username') || '',
    };
  },
  methods: {
    getSections() {
      const path = 'http://127.0.0.1:5000/sections';
      axios.get(path)
        .then((res) => {
          this.sections = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getBook() {
      const path = 'http://127.0.0.1:5000/getbooks';
      axios.get(path)
        .then((res) => {
          const booksData = res.data.books;
          this.sections.forEach((section) => {
            section.books = booksData.filter((book) => book.section_name === section.name);
          });
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getUser() {
      if (this.username) {
        return;
      }
      const token = localStorage.getItem('access_token');
      if (!token) {
        console.error('Token not found in localStorage');
        return;
      }
      const path = 'http://127.0.0.1:5000/get_user';
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      axios.get(path, config)
        .then((res) => {
          this.username = res.data.user;
          localStorage.setItem('username', this.username);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    requestBook(bookId) {
      // Implement request book functionality
    },
    readBook(bookId) {
      // Implement read book functionality
    },
  },
  created() {
    this.getSections();
    this.getBook();
    this.getUser();
  },
};
</script>

<style scoped>
div {
  color: white;
  font-family: 'Courier New', Courier, monospace;
}

.table-container {
  max-width: 800px;
  margin: 20px auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background-color: #f8f9fa;
}

th, td {
  padding: 10px;
  border: 1px solid #dee2e6;
  text-align: left;
}

th {
  background-color: #343a40;
  color: white;
}

tbody tr:nth-child(even) {
  background-color: #e9ecef;
}
.table-container {
  max-width: 800px;
  margin: 20px auto;
  text-align: right; 
}

</style>
