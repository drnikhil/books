<template>
    <div>
      <input type="file" accept=".epub,.pdf" @change="handleFileUpload">
      <button @click="uploadFile">Upload</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        file: null
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
        

        axios.post('http://127.0.0.1:5000/upload_file', formData)
          .then(response => {
            console.log(response.data);
           
          })
          .catch(error => {
            console.error(error);
          });
      }
    }
  };
  </script>
  