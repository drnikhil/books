<template>
  
  <v-btn color="red darken-1" @click="logout">Logout</v-btn>
  <v-card color="basil">
    <v-card-title class="text-center justify-center py-6">
      <h1 class="font-weight-bold text-h2 text-basil">Librarian Dashboard</h1>
    </v-card-title>

    <v-tabs v-model="tab" bg-color="transparent" color="basil" grow>
      <v-tab v-for="item in items" :key="item" :value="item">
        {{ item }}
      </v-tab>
    </v-tabs>

    <v-window v-model="tab">
      <v-window-item v-for="item in items" :key="item" :value="item">
        <v-card color="basil" flat>
          <v-card-text v-if="item === 'Section Management'">
            <SectionList />
          </v-card-text>
          <v-card-text v-if="item === 'Book Management'">
            <LibraryPage />
          </v-card-text>
          <v-card-text v-if="item === 'Home'">
            <Count />
          </v-card-text>
        
 
        </v-card>
      </v-window-item>
    </v-window>
  </v-card>
  
</template>

<script>
import SectionList from '@/components/SectionList.vue';
import Base from '@/components/Base.vue'
import LibraryPage from '../components/LibraryPage.vue';
import Count from '../components/count.vue'
import Logout from '../components/logout.vue'

export default {
  components: {
    Base,
    SectionList,
    LibraryPage,
    Count,
    Logout
  },
  data() {
    return {
      tab: 'HOME',
      items: ['Home', 'Section Management','Book Management', 'Request/RETURN', 'MISC'],
      
    }
  },
};
</script>

<style>
.bg-basil {
  background-color: #fffbe6 !important;
}
.text-basil {
  color: #356859 !important;
}
</style>
