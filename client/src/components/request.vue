<template>
                <td>
              <button @click="requestBook(section.id)">Request Book</button>
              <button @click="readBook(section.id)" :disabled="!section.approved">Read</button>
            </td>
</template>



methods: {
    requestBook(bookId) {
       axios.post(`http://localhost:5000/request/${bookId}`, {
         user_id: this.userId // Assuming you have a userId in your component's data
       })
       .then(response => {
         if (response.data.access_token) {
           // Store the access token or handle it as needed
           console.log("Access granted:", response.data.access_token);
         } else {
           console.error("Access denied:", response.data.error);
         }
       })
       .catch(error => {
         console.error("Error requesting book:", error);
       });
    },
    // Other methods...
   }
   