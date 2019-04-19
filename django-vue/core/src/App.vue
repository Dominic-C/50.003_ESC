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
    coloursUsed : [],
    modifiableCalendarEvent: {locked:[], modifiable:[]},
    username : "",
    calendarEventTable: {  },
    courseTable:[{}]
  }),
  components: {
    SearchBar,
    ListSelection,
    FinalisedCalendar,
    SuggestibleCalendar,
    RequestableCalendar,
    ViewResultsTable
  },
  computed: {
    selectedCalendarEvents() {
      //TO CHANGE: iterating through all events to get those selected-- to do through database method eventually
      var selectedEvents = []
      for (var event of this.calendarEventTable){
        if (event.data.isSelected){
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
      for (var event of this.calendarEventTable){
        //JSON.stringify so that objects can be compared
        selectionCandidatesSet.add(JSON.stringify({    
          searchText: event.data.professor, 
          pillar: event.data.pillar}));
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
      for (var event of this.calendarEventTable){
        //JSON.stringify so that objects can be compared
        selectionCandidatesSet.add(JSON.stringify({    
          searchText: event.data.courseName, 
          pillar: event.data.pillar}));
      }
      selectionCandidatesSet.forEach(searchObject => {
        selectionCandidates.push(JSON.parse(searchObject)); //parse back to object
      }); 
      return selectionCandidates; 
    },
    locationTable() {
      var selectionCandidates = [];
      var selectionCandidatesSet = new Set();
      for (var event of this.calendarEventTable){
        //JSON.stringify so that objects can be compared
        selectionCandidatesSet.add(JSON.stringify({searchText: event.data.location}));
      }
      selectionCandidatesSet.forEach(searchObject => {
        selectionCandidates.push(JSON.parse(searchObject)); 
      });
      return selectionCandidates; 
    },
    classTable() {
      var selectionCandidates = [];
      var selectionCandidatesSet = new Set();
      for (var event of this.calendarEventTable){
        //JSON.stringify so that objects can be compared
        selectionCandidatesSet.add(JSON.stringify({    
          searchText: event.data.classEnrolled, 
          pillar: event.data.pillar}));
      }
      selectionCandidatesSet.forEach(searchObject => {
        selectionCandidates.push(JSON.parse(searchObject)); //parse back to object
      }); 
      return selectionCandidates; 
    },
    retrieveTableData(){
      var json = {}
      for(i in tables){
        json[i] = tables[i].fields;
      }
      return json;
    }
  },
  created() {
    this.$eventHub.$on('event-update', this.updateModifiable);
  },
  beforeDestroy() {
      this.$eventHub.$off('event-update');
  },
  methods: {
    getColour(){
      let colour = Colors[Math.floor(Colors.length * Math.random())].value;
      if (this.coloursUsed.length < Colors.length && this.coloursUsed.includes(colour)){
        this.getColour();
      }
      this.coloursUsed.push(colour);
      return colour;
    },
    updateCalendar(e){
      //TO CHANGE: hardcoding change--to change in database
      for (var lesson of this.calendarEventTable){
        if (lesson.data[e.searchCategory] === e.item){
          lesson.data.isSelected = e.isSelected;
          //updating modifiable calendar
          if (e.isSelected === true && lesson.data.calendarType === 'Academic'){
            //updating modifiable
            var modifiableEvent = JSON.parse(JSON.stringify(lesson)) //copying event object
            modifiableEvent.data.locked = false;
            modifiableEvent.data.suggestedBy = this.username;
            modifiableEvent.data.requestedBy = this.username; 
            this.modifiableCalendarEvent.modifiable.push(modifiableEvent);
            var lockedEvent = JSON.parse(JSON.stringify(lesson)); //copying event object
            lockedEvent.data.locked = true;
            lockedEvent.data.color = "#EBEBE4";
            this.modifiableCalendarEvent.locked.push(lockedEvent);
          }
          else if (e.isSelected === false && lesson.data.calendarType === 'Academic'){
            for (let index = 0; index < this.modifiableCalendarEvent.locked.length; index ++){
              if (this.modifiableCalendarEvent.locked[index].data.id === lesson.data.id){
                this.modifiableCalendarEvent.locked.splice(index, 1); 
                this.modifiableCalendarEvent.modifiable.splice(index, 1);
              }
            }

          }
        }
      }
    },
    revertState(){
      for (let index = 0; index < this.modifiableCalendarEvent.locked.length; index ++){
        var event = JSON.parse(JSON.stringify(this.modifiableCalendarEvent.locked[index]));
        event.data.locked = false;
        event.data.color = this.modifiableCalendarEvent.modifiable[index].data.color;
        this.modifiableCalendarEvent.modifiable[index] = event; 
      }
      this.$eventHub.$emit('apply-events');
    },
    updateModifiable(event){
      for (let index = 0; index < this.modifiableCalendarEvent.modifiable.length; index ++){
        if (event.data.id === this.modifiableCalendarEvent.modifiable[index].data.id){
          const updatedEventData = {...this.modifiableCalendarEvent.modifiable[index].data, ...event.data };
          this.modifiableCalendarEvent.modifiable[index] = {data: updatedEventData, schedule: event.schedule};
        }
      }
    }
  }
};
</script>

<style>
</style>
