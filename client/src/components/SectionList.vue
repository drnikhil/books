<template>
  <div class="section-list">
    <h2>Sections</h2>
    <ul>
      <li v-for="section in sections" :key="section.id">
        <span>{{ section.name }}</span> - <span>{{ section.description }}</span>
        <button @click="editSection(section)" class="delete-button">Edit</button>
        <button @click="deleteSection(section)" class="update-button">Delete</button>
      </li>
    </ul>

    <form v-if="isEditing" @submit.prevent="updateSection">
      <label>Name:</label>
      <input type="text" v-model="updatedSection.name" required class="form-input">
      <label>Description:</label>
      <input type="text" v-model="updatedSection.description" required class="form-input">
      <button type="submit" class="update-button">Update Section</button>
    </form>

    <form v-else @submit.prevent="addSection">
      <label>Name:</label>
      <input type="text" v-model="newSection.name" required class="form-input">
      <label>Description:</label>
      <input type="text" v-model="newSection.description" required class="form-input">
      <button type="submit" class="add-button">Add Section</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      sections: [],
      newSection: {
        name: '',
        description: '',
      },
      updatedSection: {
        id: null,
        name: '',
        description: '',
      },
      isEditing: false,
    };
  },
  created() {
    this.fetchSections();
  },
  methods: {
    fetchSections() {
      axios.get('http://127.0.0.1:5000/sections')
        .then(response => {
          this.sections = response.data;
        })
        .catch(error => {
          console.error('Error fetching sections:', error);
        });
    },
    addSection() {
      axios.post('http://127.0.0.1:5000/add_section', this.newSection)
        .then(response => {
          this.fetchSections();
          this.newSection.name = '';
          this.newSection.description = '';
        })
        .catch(error => {
          console.error('Error adding section:', error);
        });
    },
    editSection(section) {
      this.isEditing = true;
      this.updatedSection.id = section.id;
      this.updatedSection.name = section.name;
      this.updatedSection.description = section.description;
    },
    updateSection() {
      axios.post(`http://127.0.0.1:5000/update_section/${this.updatedSection.id}`, this.updatedSection)
        .then(response => {
          this.fetchSections();
          this.isEditing = false;
          this.updatedSection.id = null;
          this.updatedSection.name = '';
          this.updatedSection.description = '';
        })
        .catch(error => {
          console.error('Error updating section:', error);
        });
    },
    deleteSection(section) {
      axios.delete(`http://127.0.0.1:5000/delete_section/${section.id}`)
        .then(response => {
          this.fetchSections();
        })
        .catch(error => {
          console.error('Error deleting section:', error);
        });
    },
  },
};
</script>

<style scoped>
.section-list {
  background-color: #303030;
  color: white;
  padding: 20px;
}

.delete-button {
  color: red;
}

.update-button {
  color: green;
}

.form-input {
  color: white;
  margin-bottom: 10px;
}
</style>
