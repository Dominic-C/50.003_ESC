<template>
  <div id="schedule">
    <v-app id="dayspan" v-cloak>
      <v-content>
        <search-bar
          :calendarEventsTable="calendarEventTable"
          :professorTable="professorTable"
          :courseNameTable="courseNameTable"
          :locationTable="locationTable"
          :classTable="classTable"
          @selected-search-item="updateCalendar"
        ></search-bar>
        <list-selection :courseList="courseTable"></list-selection>
        <weekly-calendar-finalised :events="selectedCalendarEvents">></weekly-calendar-finalised>
        <weekly-calendar-suggestable :events="selectedCalendarEvents">></weekly-calendar-suggestable>
      </v-content>
    </v-app>
  </div>
</template>


<script>
import { Calendar, Weekday } from "dayspan";
import Colors from "dayspan-vuetify/src/colors.js";
import SearchBar from "./components/SearchBar.vue";
import ListSelection from "./components/ListSelection.vue";
import weeklyCalendarSuggestable from "./components/WeeklyCalendarSuggestable.vue";

export default {
  name: "scheduler",
  data: () => ({})
};
</script>