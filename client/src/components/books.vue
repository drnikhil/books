<template>
  <div>
     <div>
       <h2>Add Book</h2>
       <div>
         <label>Title:</label>
         <input type="text" v-model="newBook.title">
       </div>
       <div>
         <label>Content:</label>
         <textarea v-model="newBook.content"></textarea>
       </div>
       <div>
         <label>Authors:</label>
         <input type="text" v-model="newBook.authors">
       </div>
       <div>
         <label>Section:</label>
         <select v-model="newBook.section_id">
           <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
         </select>
       </div>
       <div>
         <label>Book File:</label>
         <input type="file" accept=".pdf,.epub" @change="handleFileUpload">
       </div>
       <button @click="addBook">Add Book</button>
     </div>
 
     <div>
       <h2>Books</h2>
       <ul>
         <li v-for="book in books" :key="book.id">
           <div>
             <h3>{{ book.title }}</h3>
             <p>{{ book.content }}</p>
             <p>Authors: {{ book.authors }}</p>
             <p>Section: {{ getSectionName(book.section_id) }}</p>
             <button @click="deleteBook(book.id)">Delete</button>
             <button @click="showUpdateForm(book)">Update</button>
           </div>
         </li>
       </ul>
     </div>
 
     <div v-if="showUpdate">
       <h2>Update Book</h2>
       <div>
         <label>Title:</label>
         <input type="text" v-model="updatedBook.title">
       </div>
       <div>
         <label>Content:</label>
         <textarea v-model="updatedBook.content"></textarea>
       </div>
       <div>
         <label>Authors:</label>
         <input type="text" v-model="updatedBook.authors">
       </div>
       <div>
         <label>Section:</label>
         <select v-model="updatedBook.section_id">
           <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
         </select>
       </div>
       <button @click="updateBook">Update Book</button>
       <button @click="cancelUpdate">Cancel</button>
     </div>
  </div>
 </template>
 
 <script>
 import axios from 'axios';
 
 export default {
  data() {
     return {
       books: [],
       sections: [],
       newBook: {
         title: '',
         content: '',
         authors: '',
         section_id: null,
         file: null
       },
       updatedBook: {
         id: null,
         title: '',
         content: '',
         authors: '',
         section_id: null
       },
       showUpdate: false
     };
  },
  methods: {
     mounted() {
       this.getBooks();
       this.getSections();
     },
     getBooks() {
       axios.get('http://127.0.0.1:5000/getbooks')
         .then(response => {
           this.books = response.data.books;
         })
         .catch(error => {
           console.error('Error fetching books:', error);
         });
     },
     getSections() {
       axios.get('http://127.0.0.1:5000/get_sections')
         .then(response => {
           this.sections = response.data.sections;
         })
         .catch(error => {
           console.error('Error fetching sections:', error);
         });
     },
     handleFileUpload(event) {
       this.newBook.file = event.target.files[0];
     },
     addBook() {
       const formData = new FormData();
       formData.append('title', this.newBook.title);
       formData.append('content', this.newBook.content);
       formData.append('authors', this.newBook.authors);
       formData.append('section_id', this.newBook.section_id);
       formData.append('file', this.newBook.file);
 
 
       axios.post('http://127.0.0.1:5000/add_book', formData)
         .then(() => {
           this.getBooks();
           this.newBook = {
             title: '',
             content: '',
             authors: '',
             section_id: null,
             file: null
           };
         })
         .catch(error => {
           console.error('Error adding book:', error);
         });
     },
     deleteBook(bookId) {
       axios.delete(`http://127.0.0.1:5000/delete_book/${bookId}`)
         .then(() => {
           this.getBooks();
         })
         .catch(error => {
           console.error('Error deleting book:', error);
         });
     },
     showUpdateForm(book) {
       this.updatedBook.id = book.id;
       this.updatedBook.title = book.title;
       this.updatedBook.content = book.content;
       this.updatedBook.authors = book.authors;
       this.updatedBook.section_id = book.section_id;
       this.showUpdate = true;
     },
     updateBook() {
       axios.put(`http://127.0.0.1:5000/update_book/${this.updatedBook.id}`, this.updatedBook)
         .then(() => {
           this.getBooks();
           this.cancelUpdate();
         })
         .catch(error => {
           console.error('Error updating book:', error);
         });
     },
     cancelUpdate() {
       this.showUpdate = false;
       this.updatedBook = {
         id: null,
         title: '',
         content: '',
         authors: '',
         section_id: null
       };
     },
     getSectionName(sectionId) {
       const section = this.sections.find(s => s.id === sectionId);
       return section ? section.name : 'Unknown';
     }
  }
 };
 </script>