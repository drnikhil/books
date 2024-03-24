<template>
  <div>
    <Search/>
    <Logout />
    <div class="background">
      <div>Welcome Bookworm {{ username }}</div>
      <div class="books-container">
        <div v-for="section in sections" :key="section.id" class="section">
          <h3>{{ section.name }}</h3>
          <div v-if="section.books && section.books.length" class="books">
            <div v-for="book in section.books" :key="book.id" class="book">
              <div class="book-details">
                <div class="book-name">{{ book.name }}</div>
                <div class="book-authors">{{ book.authors }}</div>
                <div class="book-status">{{ book.status }}</div>
              </div>
              <div class="book-actions">
                <button @click="requestBook(book.book_id)">Request Book</button>
                <button @click="openBookDetails(book.book_id)">Book Details</button>
              </div>
            </div>
          </div>
          <div v-else>No books available</div>
        </div>
      </div>
    </div>
    <div class="book-details2" v-if="bookDetails">
      <h2>Book Details</h2>
      <p><strong>Content:</strong> {{ bookDetails.content }}</p>
      <p><strong>File Path:</strong> <a :href="bookDetails.filePath" target="_blank">{{ getFileName(bookDetails.filePath) }}</a></p>
      <div v-html="renderIframe(bookDetails.filePath)"></div>
    </div> 
    <div v-else>
      <p>Check whether you are allowed to view this</p>
    </div> 
  </div>
</template>

<script>
import axios from 'axios';
import Logout from '../components/logout.vue';
import Search from '../components/search.vue';

export default {
  name: 'UserDashboard',
  components: {
    Search,
    Logout,
  },
  data() {
    return {
      sections: [],
      username: localStorage.getItem('username') || '',
      bookDetails: null,
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
    getBooks() {
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
      if (!this.username) {
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
            this.username = res.data.username;
            localStorage.setItem('username', this.username);
            localStorage.setItem('user_id', res.data.user_id);
          })
          .catch((error) => {
            console.error(error);
          });
      }
    },
    requestBook(bookId) {
      const userId = localStorage.getItem('user_id');
      const path = `http://127.0.0.1:5000/requestbook`;
      const data = {
        book_id: bookId,
        user_id: userId
      };
      console.log('Request Data:', data);
      axios.post(path, data)
        .then((res) => {
          console.log('Response:', res.data.message);
          if (res.data.rental_id) {
            this.openBookDetails(res.data.rental_id);
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    openBookDetails(rental_id) {
      const rentalId = rental_id;
      axios.get(`http://127.0.0.1:5000/bookdetails/${rentalId}`)
        .then(response => {
          const bookDetails = response.data;
          const filePath = bookDetails.file_path;
          bookDetails.filePath = `http://127.0.0.1:5000/uploads/${filePath}`;
          this.bookDetails = bookDetails;
        })
        .catch(error => {
          console.error('Error fetching book details:', error);
        });
    },
    renderIframe(filePath) {
      return `<iframe src="${filePath}" width="100%" height="600px" frameborder="0"></iframe>`;
    },
    getFileName(filePath) {
      const pathSegments = filePath.split(/\\|\//); 
      return pathSegments[pathSegments.length - 1];
    },
  },
  created() {
    this.getSections();
    this.getBooks();
    this.getUser();
  },
};
</script>

<style scoped>
.background {
  background-color: #f4ede6;
  padding: 20px;
}

.books-container {
  display: flex;
  flex-wrap: wrap;
}

.section {
  flex: 1 0 33.33%;
  padding: 10px;
}

.book {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}

.book-details {
  margin-bottom: 10px;
}

.book-details2 {
  color: brown;
  background-color: beige;
}

.book-name {
  font-weight: bold;
}

.book-actions button {
  margin-top: 5px;
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  cursor: pointer;
}

.book-actions button:hover {
  background-color: #45a049;
}
</style>
