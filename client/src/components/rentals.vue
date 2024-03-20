<template>
  <div class="rental-container">
    <h2>Rental Requests</h2>
    <table>
      <thead>
        <tr>
          <th>Request</th>
          <th>User ID</th>
          <th>Book ID</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in rentalRequests" :key="request.id">
          <td>{{ request.id }}</td>
          <td>{{ request.borrower_id }}</td>
          <td>{{ request.book_id }}</td>
          <td>{{ getStatus(request) }}</td>
          <td>
            <button @click="approveRequest(request.id)">Grant</button>
            <button @click="revokeAccess(request.id)">Revoke</button>
            <button @click="deleteRequest(request.id)">Delete Request</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      rentalRequests: [],
    };
  },
  created() {
    this.fetchRentalRequests();
  },
  methods: {
    fetchRentalRequests() {
      axios.get('http://127.0.0.1:5000/rentals')
        .then(response => {
          this.rentalRequests = response.data;
        })
        .catch(error => {
          console.error('Error fetching rental requests:', error);
        });
    },
    getStatus(request) {
      if (request.approved) {
        return 'Approved';
      } else if (request.returned) {
        return 'Revoked';
      } else {
        return 'Pending';
      }
    },
    approveRequest(rentalId) {
      axios.put(`http://127.0.0.1:5000/approve/${rentalId}`)
        .then(response => {
          console.log('Rental request approved:', response.data);
          this.fetchRentalRequests();
        })
        .catch(error => {
          console.error('Error approving rental request:', error);
        });
    },
    revokeAccess(rentalId) {
      axios.put(`http://127.0.0.1:5000/revoke_access/${rentalId}`)
        .then(response => {
          console.log('Access revoked for rental:', response.data);
          this.fetchRentalRequests();
        })
        .catch(error => {
          console.error('Error revoking access for rental:', error);
        });
    },
    deleteRequest(rentalId) {
      axios.delete(`http://127.0.0.1:5000/delete_rental/${rentalId}`)
        .then(response => {
          console.log('Rental request deleted:', response.data);
          this.fetchRentalRequests();
        })
        .catch(error => {
          console.error('Error deleting rental request:', error);
        });
    }
  }
};
</script>

<style scoped>
.rental-container {
  max-width: 800px;
  margin: 20px auto;
}

table {
  width: 100%;
  border-collapse: collapse;
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

tr:nth-child(even) {
  background-color: #f8f9fa;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  cursor: pointer;
  margin-right: 5px;
}

button:hover {
  background-color: #0056b3;
}
</style>
