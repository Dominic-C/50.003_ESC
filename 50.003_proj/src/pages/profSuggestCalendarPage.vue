<template>
    <v-app id="dayspan" v-cloak>
      <app-header @changeComp="toggleVisible"></app-header>
      <v-content>
        <search-courses></search-courses>
        <weekly-calendar-suggestable></weekly-calendar-suggestable>
      </v-content>
    </v-app>
</template>

<script>
import AppHeader from "../components/AppHeader.vue";
import SearchCourses from '../components/SearchCourses.Vue'
import WeeklyCalendarSuggestable from '../components/WeeklyCalendarSuggestable.vue';

export default {
    components: {
        AppHeader,
        SearchCourses, 
        WeeklyCalendarSuggestable
    }
}
</script>
