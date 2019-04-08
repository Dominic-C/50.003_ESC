<template>
    <v-app id="dayspan" v-cloak>
      <app-header @changeComp="toggleVisible"></app-header>
      <v-content>
        <search-bar></search-bar>
        <weekly-calendar-finalised></weekly-calendar-finalised>
      </v-content>
    </v-app>
</template>

<script>
import AppHeader from "../components/AppHeader.vue"
import SearchBar from '../components/SearchBarVue'
import WeeklyCalendarFinalised from '../components/WeeklyCalendarFinalised.vue';
import AppHeaderVue from '../components/AppHeader.vue';

export default {
    components: {
        AppHeader,
        SearchBar, 
        WeeklyCalendarFinalised
    }
}
</script>
