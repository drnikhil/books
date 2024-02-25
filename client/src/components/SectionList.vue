<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'SectionList',
  props: {
    sections: {
      type: Array,
      required: true,
    },
  },
});
</script>

<template>
  <div>
    <h2>Sections</h2>
    <ul>
      <li v-for="section in sections" :key="section.id">
        {{ section.name }}
        {{ section.description }}
      </li>
    </ul>
  </div>
</template>