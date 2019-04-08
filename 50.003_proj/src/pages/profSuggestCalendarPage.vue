<template>
    <v-app id="dayspan" v-cloak>
      <app-header @changeComp="toggleVisible"></app-header>
      <v-content>
        <search-bar></search-bar>
        <weekly-calendar-suggestable></weekly-calendar-suggestable>
      </v-content>
    </v-app>
</template>

<script>
import AppHeader from "../components/AppHeader.vue";
import SearchBar from '../components/SearchBar.Vue'
import WeeklyCalendarSuggestable from '../components/WeeklyCalendarSuggestable.vue';

export default {
    components: {
        AppHeader,
        SearchBar, 
        WeeklyCalendarSuggestable
    }
}
</script>
