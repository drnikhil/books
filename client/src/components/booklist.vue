<template>
    <div class="bookslist">
        <div v-for="book in books" :key="book.name">
            <h3>{{ book.name }}</h3>
            <p><strong>Authors:</strong> {{ book.authors }}</p>
            <p><strong>Content:</strong> {{ book.content }}</p>
            <p><strong>Section:</strong> {{ book.section_name }}</p>
        </div>
    </div>
</template>


<script>
import axios from 'axios';

export default {
    name: 'BooksList',
    components: {
        
    },
    data() {
        return {
            books: []
        };
    },
    methods: {
        fetchBooks() {
            const path = 'http://127.0.0.1:5000/getbooks';
            axios.get(path)
                .then((res) => {
                    this.books = res.data.books;
                })
                .catch((error) => {
                    console.error('Error fetching books:', error);
                });
        }
    },
    created() {
        this.fetchBooks();
    }
};
</script>

<style scoped>

</style>