<template>
  <div class="container">
    <button type="button" class="btn btn-primary message-button">{{ msg }}</button>
    <Search/>

  
  </div>
</template>

<script>
import axios from 'axios';
import Search from '../components/search.vue' 

export default {
  name: 'Home',
  components: {
    Search,
  },
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>

<style>
body {
  background-image: url('../assets/background.png');
  background-size: cover;
}
</style>
