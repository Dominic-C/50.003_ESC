<template>
    <v-app id="dayspan" v-cloak>
      <app-header @changeComp="toggleVisible"></app-header>
      <v-content>
        <search-courses></search-courses>
        <weekly-calendar-finalised></weekly-calendar-finalised>
      </v-content>
    </v-app>
</template>

<script>
import AppHeader from "../components/AppHeader.vue"
import SearchCourses from '../components/SearchCoursesVue'
import WeeklyCalendarFinalised from '../components/WeeklyCalendarFinalised.vue';
import AppHeaderVue from '../components/AppHeader.vue';

export default {
    components: {
        AppHeader,
        SearchCourses, 
        WeeklyCalendarFinalised
    }
}
</script>
