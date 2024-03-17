<template>
  <div>
     <input type="file" accept=".epub,.pdf" @change="handleFileUpload">
     <v-col cols="12" md="4" sm="6">
       <v-btn @click="uploadFile" rounded="0" small block color="primary" dark>Upload</v-btn>
     </v-col>
  </div>
 </template>
 
 <script>
 import axios from 'axios'; 
 
 export default {
  name: 'Upload',
  props: ['bookId'],
 
  data() {
     return {
       file: null,
       file_path: null
     };
  },
  methods: {
     handleFileUpload(event) {
       this.file = event.target.files[0];
     },
     uploadFile() {
       if (!this.file) {
         console.error('No file selected');
         return;
       }
 
       const formData = new FormData();
       formData.append('file', this.file);
 
       axios.post(`http://127.0.0.1:5000/upload_file/${this.bookId}`, formData, {
         headers: {
           'Content-Type': 'multipart/form-data' 
         }
       })
       .then(response => {
         console.log('Uploading file for book ID:', this.bookId);
         console.log(response.data);
         this.file_path = response.data.file_path; 
         this.$emit('fileUploaded', this.file_path); 
       })
       .catch(error => {
         console.error(error);
       });
     }
  }
 };
 </script>
 