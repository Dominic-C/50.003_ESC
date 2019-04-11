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
        <suggestible-calendar
          ref="suggestCalendar"
          :events="modifiableCalendarEvent"
          :username="username"
          @revert-state="revertState"
          @event-update="updateModifiable"
          v-if="activeComp.viewTimetableToSuggest"
        ></suggestible-calendar>
        <requestable-calendar
          ref="requestCalendar"
          :events="modifiableCalendarEvent"
          :username="username"
          @revert-state="revertState"
          @event-update="updateModifiable"
          v-if="activeComp.requestChangesToCalendar"
        ></requestable-calendar>
      </v-content>
    </v-app>
  </div>
</template>


<script>
import { Calendar, Weekday } from "dayspan";
import Colors from "dayspan-vuetify/src/colors.js";
import SearchBar from "./components/SearchBar.vue";
import ListSelection from "./components/ListSelection.vue";
import FinalisedCalendar from "./components/FinalisedCalendar.vue";
import SuggestibleCalendar from "./components/SuggestibleCalendar.vue";
import RequestableCalendar from "./components/RequestableCalendar.vue";

export default {
  name: "scheduler",
  components: {
    SearchBar,
    ListSelection,
    weeklyCalendarSuggestable,
    weeklyCalendarFinalised
  },
  data: () => ({
    calendar: Calendar.weeks(),
    coloursUsed: [],
    suggestibleCalendarEvents: { locked: [], suggestible: [] },
    calendarEventTable: { calendarEvents },
    courseTable: { courses }
  }),
  computed: {
    selectedCalendarEvents() {
      //TO CHANGE: iterating through all events to get those selected-- to do through database method eventually
      var selectedEvents = [];
      for (var event of this.calendarEventTable) {
        if (event.data.isSelected) {
          selectedEvents.push(event);
        }
      }
      return selectedEvents;
    },
    //other database tables
    //TO CHANGE: get from database eventually
    professorTable() {
      var selectionCandidates = [];
      var selectionCandidatesSet = new Set();
      for (var event of this.calendarEventTable) {
        //JSON.stringify so that objects can be compared
        selectionCandidatesSet.add(
          JSON.stringify({
            searchText: event.data.professor,
            pillar: event.data.pillar
          })
        );
      }
      selectionCandidatesSet.forEach(searchObject => {
        //parse back to object
        selectionCandidates.push(JSON.parse(searchObject));
      });
      return selectionCandidates;
    },
    courseNameTable() {
      var selectionCandidates = [];
      var selectionCandidatesSet = new Set();
      for (var event of this.calendarEventTable) {
        //JSON.stringify so that objects can be compared
        selectionCandidatesSet.add(
          JSON.stringify({
            searchText: event.data.courseName,
            pillar: event.data.pillar
          })
        );
      }
      selectionCandidatesSet.forEach(searchObject => {
        selectionCandidates.push(JSON.parse(searchObject)); //parse back to object
      });
      return selectionCandidates;
    },
    locationTable() {
      var selectionCandidates = [];
      var selectionCandidatesSet = new Set();
      for (var event of this.calendarEventTable) {
        //JSON.stringify so that objects can be compared
        selectionCandidatesSet.add(
          JSON.stringify({ searchText: event.data.location })
        );
      }
      selectionCandidatesSet.forEach(searchObject => {
        selectionCandidates.push(JSON.parse(searchObject));
      });
      return selectionCandidates;
    },
    classTable() {
      var selectionCandidates = [];
      var selectionCandidatesSet = new Set();
      for (var event of this.calendarEventTable) {
        //JSON.stringify so that objects can be compared
        selectionCandidatesSet.add(
          JSON.stringify({
            searchText: event.data.classEnrolled,
            pillar: event.data.pillar
          })
        );
      }
      selectionCandidatesSet.forEach(searchObject => {
        selectionCandidates.push(JSON.parse(searchObject)); //parse back to object
      });
      return selectionCandidates;
    }
  },
  methods: {
    getColour() {
      let colour = Colors[Math.floor(Colors.length * Math.random())].value;
      if (
        this.coloursUsed.length < Colors.length &&
        this.coloursUsed.includes(colour)
      ) {
        this.getColour();
      }
      this.coloursUsed.push(colour);
      return colour;
    },
    updateCalendar(e) {
      //TO CHANGE: hardcoding change--to change in database
      for (var lesson of this.calendarEventTable) {
        if (lesson.data[e.searchCategory] === e.item) {
          lesson.data.isSelected = e.isSelected;
          //updating suggestible calendar
          if (
            e.isSelected === true &&
            lesson.data.calendarType === "Academic"
          ) {
            var suggestingEvent = JSON.parse(JSON.stringify(lesson)); //copying event object
            suggestingEvent.data.locked = false;
            suggestingEvent.data.suggestedBy = "username"; //TO CHANGE: replace with username
            this.suggestibleCalendarEvents.suggestible.push(suggestingEvent);
            var lockedEvent = JSON.parse(JSON.stringify(lesson)); //copying event object
            lockedEvent.data.locked = true;
            lockedEvent.data.color = "#EBEBE4";
            this.suggestibleCalendarEvents.locked.push(lockedEvent);
          } else if (
            e.isSelected === false &&
            lesson.data.calendarType === "Academic"
          ) {
            for (
              let index = 0;
              index < this.suggestibleCalendarEvents.locked.length;
              index++
            ) {
              if (
                this.suggestibleCalendarEvents.locked[index].data.id ===
                lesson.data.id
              ) {
                this.suggestibleCalendarEvents.locked.splice(index, 1);
                this.suggestibleCalendarEvents.suggestible.splice(index, 1);
              }
            }
          }
        }
      }
    },
    revertState() {
      for (
        let index = 0;
        index < this.suggestibleCalendarEvents.locked.length;
        index++
      ) {
        var event = JSON.parse(
          JSON.stringify(this.suggestibleCalendarEvents.locked[index])
        );
        event.data.locked = false;
        this.suggestibleCalendarEvents.suggestible[index] = event;
      }
      this.$refs.suggestCalendar.applyEvents();
    },
    updateSuggestible(event) {
      for (
        let index = 0;
        index < this.suggestibleCalendarEvents.suggestible.length;
        index++
      ) {
        if (
          event.data.id ===
          this.suggestibleCalendarEvents.suggestible[index].data.id
        ) {
          const updatedEventData = {
            ...this.suggestibleCalendarEvents.suggestible[index].data,
            ...event.data
          };
          this.suggestibleCalendarEvents.suggestible[index] = {
            data: updatedEventData,
            schedule: event.schedule
          };
        }
      }
    }
  }
};
</script>