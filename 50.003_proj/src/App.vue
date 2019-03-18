<template>
  <v-app id="dayspan" v-cloak>
    <ds-calendar-app :calendar="calendar"></ds-calendar-app>
    <Courses />
    
  </v-app>
</template>

<script>
import { Calendar } from 'dayspan';
import Courses from './components/Courses.vue';

export default {
  name: 'app',
  data: () => ({
    calendar: Calendar.weeks()
  }),
  components: {
    Courses
  }
}
</script>

<style>
body, html, #app, #dayspan {
  font-family: Roboto, sans-serif;
  width: 100%;
  height: 100%;
}
</style>