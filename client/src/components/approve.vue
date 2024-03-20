<template>
    <div>
      <h2>Rental Requests</h2>
      <table class="rental-table">
        <thead>
          <tr>
            <th>User</th>
            <th>Book Requested</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in rentalRequests" :key="request.id">
            <td>{{ request.user_id }}</td>
            <td>{{ request.book_id }}</td>
            <td>
              <button @click="approveRequest(request.id)" v-if="!request.approved" class="approve-button">Approve</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: "Approve",
    data() {
      return {
        rentalRequests: []
      };
    },
    mounted() {
      this.fetchRentalRequests();
    },
    methods: {
      fetchRentalRequests() {
        axios.post('http://127.0.0.1:5000/requestbook',  {
            headers: {
                'Content-Type': 'application/json'
            }
        })
          .then(response => {
            this.rentalRequests = response.data;
          })
          .catch(error => {
            console.error('Error fetching rental requests:', error);
          });
      },
      approveRequest(requestId) {
        axios.put(`http://127.0.0.1:5000/approve/${requestId}`)
          .then(response => {
            if (response.status === 200) {
              const requestIndex = this.rentalRequests.findIndex(request => request.id === requestId);
              if (requestIndex !== -1) {
                this.$set(this.rentalRequests[requestIndex], 'approved', true);
              }
            } else {
              console.error('Failed to approve rental request:', response.statusText);
            }
          })
          .catch(error => {
            console.error('Error approving rental request:', error);
          });
      }
    }
  };
  </script>
  
  <style scoped>
  .rental-table {
    width: 100%;
    border-collapse: collapse;
    color:brown
  }
  
  .rental-table th, .rental-table td {
    padding: 8px;
    border: 1px solid #dddddd;
  }
  
  .rental-table th {
    background-color: #f2f2f2;
    font-weight: bold;
    text-align: left;
  }
  
  .rental-table td {
    text-align: center;
  }
  
  .approved {
    color: green;
  }
  
  .pending {
    color: orange;
  }
  
  .approve-button {
    padding: 6px 10px;
    border: none;
    background-color: #007bff;
    color: white;
    cursor: pointer;
    border-radius: 4px;
  }
  
  .approve-button:hover {
    background-color: #0056b3;
  }
  </style>
  