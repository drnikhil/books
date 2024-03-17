<template>
    <div>
      <h1>User Dashboard</h1>
      <button @click="downloadResource" :disabled="isWaiting">Download Resource</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'User',
    data() {
      return {
        isWaiting: false 
      };
    },
    methods: {
      async downloadResource() {
        try {
          this.isWaiting = true; 
          const response = await axios.get('/dload_csv');
          const taskId = response.data['task-id'];
  
          const interval = setInterval(async () => {
            try {
              const csvRes = await axios.get(`/get_csv/${taskId}`);
              if (csvRes.status === 200) {
                clearInterval(interval);
                window.location.href = `/get_csv/${taskId}`;
                this.isWaiting = false; 
              }
            } catch (error) {
              console.error('Error checking task status:', error);
            }
          }, 1000);
        } catch (error) {
          console.error('Error initiating download:', error);
          this.isWaiting = false; 
        }
      }
    }
  };
  </script>
  
  <style scoped>
  
  </style>
  