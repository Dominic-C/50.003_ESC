<template>
  <div id="app">
    <v-app id="dayspan" v-cloak>
      <v-content>
        <v-layout row wrap>
          <v-flex xs4 pa-4>
            <v-select
              single-line
              solo
              flat
              label="Phase"
              :items="[{text:'1', value: 1}, {text:'2', value: 2}, {text:'3', value: 3}]"
              v-model="phase"
            ></v-select>
          </v-flex>

          <v-flex xs4 pa-4>
            <v-select
              single-line
              solo
              flat
              label="User"
              :items="['Professor', 'Admin', 'Course Coordinator', 'Student', 'Timetable Planner']"
              v-model="user"
            ></v-select>
          </v-flex>
        </v-layout>

        <search-bar
          :calendarEventsTable="calendarEventTable"
          :professorTable="professorTable"
          :courseNameTable="courseNameTable"
          :locationTable="locationTable"
          :classTable="classTable"
          @selected-search-item="updateCalendar"
          v-if="(phase === 2 || phase === 3)"
        ></search-bar>
        <!-- <list-selection :courseList="courseTable" v-if="activeComp.courseListingForViewer"></list-selection> -->
        <!-- <weekly-calendar :courseList="courseList" v-if="false"></weekly-calendar> -->
        <finalised-calendar :events="selectedCalendarEvents" v-if="phase===3"></finalised-calendar>
        <suggestible-calendar
          :events="modifiableCalendarEvent"
          :username="username"
          @revert-state="revertState"
          @suggested="updateSuggested"
          v-if="phase===2 &&
            user==='Professor'"
        ></suggestible-calendar>
        <requestable-calendar
          :events="modifiableCalendarEvent"
          :username="username"
          @revert-state="revertState"
          @requested="updateRequested"
          v-if="phase===3 &&
            user==='Professor'"
        ></requestable-calendar>
        <approve-table
          :username="username"
          :possibleConflictingEvents="possibleConflictingEvents"
          :suggesting="true"
          :suggestions="suggestibleTable"
          user="Course Coordinator"
          @view-conflicts="updateConflicts"
          v-if="phase===2 &&
            user==='Course Coordinator'"
        ></approve-table>
        <view-status-table
          :username="username"
          :possibleConflictingEvents="possibleConflictingEvents"
          :suggesting="true"
          :suggestions="suggestibleTable"
          user="Professor"
          @view-conflicts="updateConflicts"
          v-if="phase===2 &&
            user==='Professor'"
        ></view-status-table>
        <approve-table
          :username="username"
          :possibleConflictingEvents="possibleConflictingEvents"
          :suggesting="false"
          :suggestions="suggestibleTable"
          @view-conflicts="updateConflicts"
          user="Course Coordinator"
          v-if="phase===2 &&
            user==='Course Coordinator'"
        ></approve-table>
        <view-status-table
          :username="username"
          :possibleConflictingEvents="possibleConflictingEvents"
          :suggesting="false"
          :suggestions="suggestibleTable"
          user="Professor"
          @view-conflicts="updateConflicts"
          v-if="phase===3 &&
            user==='Professor'"
        ></view-status-table>
      </v-content>
    </v-app>
  </div>
</template>

<script>
import { Weekday } from "dayspan";
import * as moment from "moment";
import Colors from "dayspan-vuetify/src/colors.js";

import SearchBar from "./components/SearchBar.vue";
import ListSelection from "./components/ListSelection.vue";

import FinalisedCalendar from "./components/FinalisedCalendar.vue";
import RequestableCalendar from "./components/RequestableCalendar.vue";
import SuggestibleCalendar from "./components/SuggestibleCalendar.vue";
// import ViewResultsTable from "./components/ViewResultsTable";

import ApproveTable from "./components/ApproveTable";
import ViewStatusTable from "./components/ViewStatusTable";
import FormSubmit from "./components/FormSubmit.vue";

export default {
  name: "app",
  data: () => ({
    coloursUsed: [],
    coloursMap: new Map(),
    modifiableCalendarEvent: { locked: [], modifiable: [] },
    possibleConflictingEvents: [],
    suggestibleTable: [],
    requestableTable: [],
    username: "user",
    mappedEventsTable: json,
    phase: planningPhase,
    user: userlogged
  }),
  components: {
    SearchBar,
    FormSubmit,
    ListSelection,
    FinalisedCalendar,
    SuggestibleCalendar,
    RequestableCalendar,
    ApproveTable,
    ViewStatusTable
  },
  computed: {
    calendarEventTable() {
      return [{}];
    },
    selectedCalendarEvents() {
      //TO CHANGE: iterating through all events to get those selected-- to do through database method eventually
      var selectedEvents = [];
      for (var event of this.mappedEventsTable) {
        if (event.data.isSelected) {
          selectedEvents.push(event);
        }
        console.log(event.data.isSelected);
      }
      return selectedEvents;
    },
    //other database tables
    //TO CHANGE: get from database eventually
    professorTable() {
      var selectionCandidates = [];
      var selectionCandidatesSet = new Set();
      for (var event of this.mappedEventsTable) {
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
      for (var event of this.mappedEventsTable) {
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
      for (var event of this.mappedEventsTable) {
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
      for (var event of this.mappedEventsTable) {
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
    },
    mapCalendarEventsTable() {
      // Mapping the simple Table -> calendar type table
      var json = [];
      for (var i = 0; i < simpleTable.length; i++) {
        var tempdata = {};
        var tempschedule = {};
        tempdata["courseName"] = simpleTable[i].course_Name;
        tempdata["pillar"] = simpleTable[i].pillar_Type;
        tempdata["id"] = i;
        tempdata["eventName"] = simpleTable[i].event_Name;
        tempdata["color"] = "#1976d2";
        tempdata["location"] = simpleTable[i].location;
        tempdata["professor"] = simpleTable[i].lecturer;
        tempdata["classEnrolled"] = simpleTable[i].class_Enrolled;
        tempdata["calendarType"] = simpleTable[i].is_Event
          ? "Event"
          : "Academic";
        tempdata["locked"] = false;
        tempdata["suggestedBy"] = simpleTable[i].initiated_By;
        tempdata["requestedBy"] = simpleTable[i].initiated_By;
        tempdata["isSelected"] = false;

        tempschedule["dayOfWeek"] = [simpleTable[i].day_Of_Week];
        tempschedule["times"] = [simpleTable[i].start_Time];
        tempschedule["duration"] = simpleTable[i].event_Duration;
        tempschedule["durationUnit"] = "minutes";
        tempschedule["exclude"] = [];
        tempschedule["start"] = [];
        tempschedule["end"] = [];

        var pair = {
          data: tempdata,
          schedule: tempschedule
        };
        json[i] = pair;
      }
      return json;
    }
  },
  created() {
    this.$eventHub.$on("event-update", this.updateModifiable);
  },
  beforeDestroy() {
    this.$eventHub.$off("event-update");
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
      for (var lesson of this.mappedEventsTable) {
        if (lesson.data[e.searchCategory] === e.item) {
          lesson.data.isSelected = e.isSelected;
          //updating modifiable calendar
          if (
            e.isSelected === true &&
            lesson.data.calendarType === "Academic"
          ) {
            //updating modifiable
            var modifiableEvent = JSON.parse(JSON.stringify(lesson)); //copying event object
            modifiableEvent.data.locked = false;
            modifiableEvent.data.suggestedBy = this.username;
            modifiableEvent.data.requestedBy = this.username;
            this.modifiableCalendarEvent.modifiable.push(modifiableEvent);
            var lockedEvent = JSON.parse(JSON.stringify(lesson)); //copying event object
            lockedEvent.data.locked = true;
            lockedEvent.data.color = "#EBEBE4";
            this.modifiableCalendarEvent.locked.push(lockedEvent);
          } else if (
            e.isSelected === false &&
            lesson.data.calendarType === "Academic"
          ) {
            for (
              let index = 0;
              index < this.modifiableCalendarEvent.locked.length;
              index++
            ) {
              if (
                this.modifiableCalendarEvent.locked[index].data.id ===
                lesson.data.id
              ) {
                this.modifiableCalendarEvent.locked.splice(index, 1);
                this.modifiableCalendarEvent.modifiable.splice(index, 1);
              }
            }
          }
        }
      }
      // console.log(this.selectedCalendarEvents);
    },
    revertState() {
      for (
        let index = 0;
        index < this.modifiableCalendarEvent.locked.length;
        index++
      ) {
        var event = JSON.parse(
          JSON.stringify(this.modifiableCalendarEvent.locked[index])
        );
        event.data.readonly = false;
        event.data.color = this.modifiableCalendarEvent.modifiable[
          index
        ].data.color;
        this.modifiableCalendarEvent.modifiable[index] = event;
      }
      this.$eventHub.$emit("apply-events");
    },
    updateModifiable(event) {
      for (
        let index = 0;
        index < this.modifiableCalendarEvent.modifiable.length;
        index++
      ) {
        if (
          event.data.id ===
          this.modifiableCalendarEvent.modifiable[index].data.id
        ) {
          const updatedEventData = {
            ...this.modifiableCalendarEvent.modifiable[index].data,
            ...event.data
          };
          this.modifiableCalendarEvent.modifiable[index] = {
            data: updatedEventData,
            schedule: event.schedule
          };
        }
      }
    },
    updateConflicts(item) {
      this.possibleConflictingEvents = [];
      if (item.locationConflict) {
        for (var lessonLocation of this.mappedEventsTable) {
          //TO CHANGE: hardcoding change--to change in database
          const location = item.conflict[0].data.location;
          outer_block: {
            if (lessonLocation.data.location === location) {
              for (var conflictLessonLocation of item.conflict) {
                if (conflictLessonLocation.data.id === lessonLocation.data.id) {
                  break outer_block; //continue checking other lessons
                }
              }
              this.possibleConflictingEvents.push(lessonLocation);
            }
          }
        }
      }
      if (item.classConflict) {
        //TO CHANGE: hardcoding change--to change in database
        for (var lessonClass of this.mappedEventsTable) {
          const classEnrolled = item.conflict[0].data.classEnrolled;
          outer_block: {
            if (lessonClass.data.classEnrolled === classEnrolled) {
              for (var conflictLessonClass of item.conflict) {
                if (conflictLessonClass.data.id === lessonClass.data.id) {
                  break outer_block; //continue checking other lessons
                }
              }
              this.possibleConflictingEvents.push(lessonClass);
            }
          }
        }
      }
      if (this.professorConflict) {
        //TO CHANGE: hardcoding change--to change in database
        for (var lessonProf of this.mappedEventsTable) {
          const professor = item.conflict[0].data.professor;
          outer_block: {
            if (lessonProf.data.professor === professor) {
              for (var conflictLessonProf of item.conflict) {
                if (conflictLessonProf.data.id === lessonProf.data.id) {
                  break outer_block; //continue checking other lessons
                }
              }
              this.possibleConflictingEvents.push(lessonProf);
            }
          }
        }
      }
    },
    //TO CHANGE: check for conflict and update database
    updateSuggested(calendar) {
      this.suggestibleTable.push({
        suggestedBy: this.username,
        calendar: calendar,
        submittedOn: moment().format("MMMM D YYYY (dddd) h:mm:ss a"),
        status: "Pending",
        locationConflict: false,
        classConflict: true,
        professorConflict: false
      });
    },
    updateRequested(calendar) {
      this.requestableTable.push({
        requestedBy: this.username,
        calendar: calendar,
        submittedOn: moment().format("MMMM D YYYY (dddd) h:mm:ss a"),
        status: "Pending",
        locationConflict: true,
        classConflict: false,
        professorConflict: false
      });
    },
    saveState() {
      let suggestible = this.suggestibleTable;
      let jsonSuggestible = JSON.stringify(suggestible);
      localStorage.setItem("suggestibleTable", jsonSuggestible);

      let requestable = this.requestableTable;
      let jsonRequestable = JSON.stringify(requestable);
      localStorage.setItem("requestableTable", jsonRequestable);
    },
    loadState() {
      let state = {};
      try {
        let savedStateSuggestible = JSON.parse(
          localStorage.getItem("suggestibleTable")
        );
        let savedStateRequestable = JSON.parse(
          localStorage.getItem("requestableTable")
        );
        if (savedStateSuggestible) {
          this.suggestibleTable.concat(savedStateSuggestible);
        }
        if (savedStateRequestable) {
          this.requestableTable.concat(savedStateRequestable);
        }
      } catch (e) {
        console.log(e);
      }
    }
  }
};
</script>

<style>
</style>
