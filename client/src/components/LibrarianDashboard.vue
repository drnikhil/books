<template>
  <div>
    <h1>Librarian Home Page</h1>
    <div>
      <h2>Sections</h2>
      <ul>
        <li v-for="section in sections" :key="section.id">
          {{ section.name }}
          {{ section.description }}
        </li>
      </ul>
    </div>
  </div>
</template>
+
  
<script>
  import SectionList from './SectionList.vue';
 


  
  export default {
    components: {

      SectionList
    },
    data() {
      return {
        sections: []
      };
    },
    created() {
      this.fetchSections();
    },
    methods: {
      fetchSections() {
        fetch('http://127.0.0.1:5000/get_sections')
          .then(response => response.json())
          .then(data => {
            this.sections = data.sections;
          })
          .catch(error => {
            console.error('Error fetching sections:', error);
          });
      },
      addSection() {
        const name = prompt('Enter the name of the new section:');
        const description = prompt('Enter the description of the new section:');
  
        if (name && description) {
          fetch('http://127.0.0.1:5000/add_section', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, description })
          })
          .then(response => {
            if (response.ok) {
              alert('Section added successfully!');
              this.fetchSections();
            } else {
              throw new Error('Failed to add section');
            }
          })
          .catch(error => {
            console.error('Error adding section:', error);
            alert('Failed to add section');
          });
        }
      },
      deleteSection(sectionId) {
        if (confirm('Are you sure you want to delete this section?')) {
          fetch(`http://127.0.0.1:5000/delete_section/${sectionId}`, {
            method: 'DELETE'
          })
          .then(response => {
            if (response.ok) {
              alert('Section deleted successfully!');
              this.fetchSections();
            } else {
              throw new Error('Failed to delete section');
            }
          })
          .catch(error => {
            console.error('Error deleting section:', error);
            alert('Failed to delete section');
          });
        }
      },
      updateSection(sectionId) {
        const newName = prompt('Enter the new name of the section:');
        const newDescription = prompt('Enter the new description of the section:');
  
        if (newName && newDescription) {
          fetch(`http://127.0.0.1:5000/update_section/${sectionId}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: newName, description: newDescription })
          })
          .then(response => {
            if (response.ok) {
              alert('Section updated successfully!');
              this.fetchSections();
            } else {
              throw new Error('Failed to update section');
            }
          })
          .catch(error => {
            console.error('Error updating section:', error);
            alert('Failed to update section');
          });
        }
      },
      addBook(sectionId) {

      const name = prompt('Enter the name of the new book:');
      const content = prompt('Enter the content of the new book:');
      const authors = prompt('Enter the authors of the new book:');
      const dateIssued = prompt('Enter the date issued of the new book:');
      const returnDate = prompt('Enter the return date of the new book:');

      if (name && content && authors && dateIssued && returnDate) {
        fetch('http://127.0.0.1:5000/add_book', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            section_id: sectionId,
            name,
            content,
            authors,
            date_issued: dateIssued,
            return_date: returnDate
          })
        })
        .then(response => {
          if (response.ok) {
            alert('Book added successfully!');
            this.fetchSections();
          } else {
            throw new Error('Failed to add book');
          }
        })
        .catch(error => {
          console.error('Error adding book:', error);
          alert('Failed to add book');
        });
      }
    },
      
      deleteBook(bookId) {
        if (confirm('Are you sure you want to delete this book?')) {
        fetch(`http://127.0.0.1:5000/delete_book/${bookId}`, {
          method: 'DELETE'
        })
        .then(response => {
          if (response.ok) {
            alert('Book deleted successfully!');
            this.fetchSections();
          } else {
            throw new Error('Failed to delete book');
          }
        })
        .catch(error => {
          console.error('Error deleting book:', error);
          alert('Failed to delete book');
        });
      }
    },
      
      updateBook(bookId) {
      const newName = prompt('Enter the new name of the book:');
      const newContent = prompt('Enter the new content of the book:');
      const newAuthors = prompt('Enter the new authors of the book:');
      const newDateIssued = prompt('Enter the new date issued of the book:');
      const newReturnDate = prompt('Enter the new return date of the book:');

      if (newName && newContent && newAuthors && newDateIssued && newReturnDate) {
        fetch(`http://127.0.0.1:5000/update_book/${bookId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: newName,
            content: newContent,
            authors: newAuthors,
            date_issued: newDateIssued,
            return_date: newReturnDate
          })
        })
        .then(response => {
          if (response.ok) {
            alert('Book updated successfully!');
            this.fetchSections();
          } else {
            throw new Error('Failed to update book');
          }
        })
        .catch(error => {
          console.error('Error updating book:', error);
          alert('Failed to update book');
        });
      }
    }
  }
};
</script>
  