<template>
  <div id="app">
    <v-app id="dayspan" v-cloak>
      <v-content>
        <search-bar
          :calendarEventsTable="calendarEventTable"
          :professorTable="professorTable"
          :courseNameTable="courseNameTable"
          :locationTable="locationTable"
          :classTable="classTable"
          @selected-search-item="updateCalendar"
          v-if="activeComp.courseListingForViewer || activeComp.viewTimetableToSuggest || activeComp.viewFinalTimetable || activeComp.requestChangesToCalendar"
        ></search-bar>
        <!-- <list-selection :courseList="courseTable" v-if="activeComp.courseListingForViewer"></list-selection> -->
        <!-- <weekly-calendar :courseList="courseList" v-if="false"></weekly-calendar> -->
        <finalised-calendar :events="selectedCalendarEvents" v-if="activeComp.viewFinalTimetable">></finalised-calendar>
        <suggestible-calendar
          ref="suggestCalendar"
          :events="modifiableCalendarEvent"
          :username="username"
          @revert-state="revertState"
          v-if="activeComp.viewTimetableToSuggest"
        ></suggestible-calendar>
        <requestable-calendar
          ref="requestCalendar"
          :events="modifiableCalendarEvent"
          :username="username"
          @revert-state="revertState"
          v-if="activeComp.requestChangesToCalendar"
        ></requestable-calendar>
        <view-results-table v-if="activeComp.viewSuggestions"></view-results-table>
      </v-content>
    </v-app>
  </div>
</template>

<script>
import { Weekday } from "dayspan";
import Colors from "dayspan-vuetify/src/colors.js";

import SearchBar from "./components/SearchBar.vue";
import ListSelection from "./components/ListSelection.vue";

import RequestableCalendar from "./components/RequestableCalendar.vue";
import FinalisedCalendar from "./components/FinalisedCalendar.vue";
import SuggestibleCalendar from "./components/SuggestibleCalendar.vue";
import ViewResultsTable from "./components/ViewResultsTable";

export default {
  name: "app",
  data: () => ({
//TODO: PUT IN DATA LOADED FROM DJANGO HERE

  }),
  components: {
    SearchBar,
    ListSelection,
    FinalisedCalendar,
    SuggestibleCalendar,
    RequestableCalendar,
    ViewResultsTable
  }
};
</script>

<style>
</style>
