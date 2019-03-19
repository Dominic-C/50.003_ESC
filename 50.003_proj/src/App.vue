<template>
  <div>
    <search-courses></search-courses>
    <list-selection></list-selection>
  </div>
</template>

<script>
import SearchCourses from './components/SearchCourses.vue';
import ListSelection from './components/ListSelection.vue';
export default {
  name: 'app',
  data: () => ({
  }),
  components: {
    SearchCourses,
    ListSelection
  }
}
</script>  