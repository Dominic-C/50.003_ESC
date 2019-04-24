<template>
  <div id="app">
    <v-app id="dayspan" v-cloak>
      <app-header @changeComp="toggleVisible"></app-header>
      <v-content>
        <v-layout row wrap>
          <v-flex xs4 pa-4>
            <v-select
              single-line solo flat
              label="Phase"
              :items="[{text:'1', value: 1}, {text:'2', value: 2}, {text:'3', value: 3}]"
              v-model="phase">
            </v-select>
          </v-flex>
          
          <v-flex xs4 pa-4>
            <v-select
              single-line solo flat
              label="User"
              :items="['Professor', 'Admin', 'Course Coordinator', 'Student', 'Timetable Planner']"
              v-model="user">
            </v-select>
          </v-flex>
        </v-layout>

        <form-submit 
          v-if="user==='Professor' && 
            phase===1 && 
            activeComp.formSubmitNewCourse"></form-submit>
        <search-bar 
          :calendarEventsTable="calendarEventTable"
          :professorTable="professorTable"
          :courseNameTable="courseNameTable"
          :locationTable="locationTable"
          :classTable="classTable"
          @selected-search-item="updateCalendar"
          v-if="(phase===2 || phase===3) && 
            (activeComp.viewTimetableToSuggest || activeComp.viewFinalTimetable || activeComp.requestChangesToCalendar)">
        </search-bar>
        <!-- <list-selection :courseList="courseTable" v-if="activeComp.courseListingForViewer"></list-selection> -->
        <!-- <weekly-calendar :courseList="courseList" v-if="false"></weekly-calendar> -->
        <finalised-calendar 
          :events="selectedCalendarEvents" 
          v-if="phase===3 && 
            activeComp.viewFinalTimetable">></finalised-calendar>
        <suggestible-calendar 
          :events="modifiableCalendarEvent"
          :username="username"
          @revert-state="revertState"
          @suggested="updateSuggested"
          v-if="phase===2 &&
            user==='Professor' &&
            activeComp.viewTimetableToSuggest"></suggestible-calendar>
        <requestable-calendar
          :events="modifiableCalendarEvent"
          :username="username"
          @revert-state="revertState"
          @requested="updateRequested"
          v-if="phase===3 &&
            user==='Professor' &&
            activeComp.requestChangesToCalendar"></requestable-calendar>
        <approve-table  
          :username="username" 
          :possibleConflictingEvents="possibleConflictingEvents"
          :suggesting="true"
          :suggestions="suggestibleTable"
          user="Course Coordinator"
          @view-conflicts="updateConflicts"
          v-if="phase===2 &&
            user==='Course Coordinator' &&
            activeComp.viewSuggestions"></approve-table>
        <view-status-table  
          :username="username" 
          :suggesting="true"
          :suggestions="suggestibleTable"
          @view-conflicts="updateConflicts"
          v-if="phase===2 &&
            user==='Professor' &&
            activeComp.viewSuggestions"></view-status-table>
        <approve-table  
          :username="username" 
          :possibleConflictingEvents="possibleConflictingEvents"
          :suggesting="false"
          :suggestions="mockData"
          @view-conflicts="updateConflicts"
          user="Course Coordinator"
          v-if="phase===3 &&
            user==='Course Coordinator' &&
            activeComp.viewExistingRequests"></approve-table>
        <view-status-table  
          :username="username" 
          :suggesting="false"
          :suggestions="mockData"
          @view-conflicts="updateConflicts"
          v-if="phase===3 &&
            user==='Professor' &&
            activeComp.viewExistingRequests"></view-status-table>
        <approve-table  
          :username="username" 
          :possibleConflictingEvents="possibleConflictingEvents"
          :suggesting="true"
          :suggestions="suggestibleTable"
          user="Timetable Planner"
          @view-conflicts="updateConflicts"
          v-if="phase===2 &&
            user==='Timetable Planner' &&
            activeComp.viewSuggestions"></approve-table>
        <approve-table  
          :username="username" 
          :possibleConflictingEvents="possibleConflictingEvents"
          :suggesting="false"
          :suggestions="mockData"
          user="Timetable Planner"
          @view-conflicts="updateConflicts"
          v-if="phase===3 &&
            user==='Timetable Planner' &&
            activeComp.viewExistingRequests"></approve-table>
        
<!-- (user==='Professor' || user==='Admin' || user==='Course Coordinator' || user==='') -->
      </v-content>
    </v-app>
  </div>
</template>

<script>
import * as moment from 'moment';
import Colors from 'dayspan-vuetify/src/colors.js';
import AppHeader from './components/AppHeader.vue';
import SearchBar from './components/SearchBar.vue';
import FinalisedCalendar from './components/FinalisedCalendar.vue'
import SuggestibleCalendar from './components/SuggestibleCalendar.vue'
import RequestableCalendar from "./components/RequestableCalendar.vue";
import ApproveTable from "./components/ApproveTable";
import ViewStatusTable from "./components/ViewStatusTable";
import FormSubmit from './components/FormSubmit.vue';

export default {
  name: 'app',
  data: () => ({
    phase: null,
    user: null,
    coloursUsed: [],
    coloursMap: new Map(),
    modifiableCalendarEvent: {locked:[], modifiable:[]},
    possibleConflictingEvents: [],
    conflicts: [],
    username: "username", //TO CHANGE: replace with username
    //TO CHANGE: get from database
    suggestibleTable: [],
    requestableTable: [],
    activeComp: {
      // Submit new Course, Export Suggestions
      formSubmitNewCourse : false,
      viewCurrSuggestions : false,
      exportCoursesForPlanner : false,
      // Suggest new timings for course
      viewTimetableToSuggest : false,
      viewSuggestions: false,
      // After Finalization activities:
      viewExistingRequests : false,
      requestChangesToCalendar : false,
      //courseListingForViewer : false,
      viewFinalTimetable : false
    },
    mockData:[
      {
        suggestedBy: 'Prof A',
        status: "Pending",
        submittedOn: moment('01 Mar 2019 09:30').format('MMMM D YYYY (dddd) h:mm:ss a'),
        locationConflict: true,
        classConflict: false,
        professorConflict: false,
        conflict: [
          {
            "data": {
              "courseName": "50.003 Elements of Software Constructions",
              "pillar": "ISTD",
              "id": "001",
              "title": "50.003 Tutorial",
              "color": "#9C27B0",
              "location": "2.501",
              "professor": "Sun Jun",
              "classEnrolled": "F01",
              "calendarType": "Academic",
              "locked": null,
              "suggestedBy": null,
              "isSelected": false
            },
            "schedule": {
              "dayOfWeek": [1],
              "times": ["09:00"],
              "duration": 60,
              "durationUnit": "minutes"
            }
          },
          {
            "data": {
              "courseName": "50.003 Elements of Software Constructions",
              "pillar": "ISTD",
              "id": "002",
              "title": "50.003 Tutorial",
              "color": "#1976d2",
              "location": "2.501",
              "professor": "Sudipta",
              "classEnrolled": "F02",
              "calendarType": "Academic",
              "locked": null,
              "suggestedBy": "Prof A",
              "isSelected": false
            },
            "schedule": {
              "dayOfWeek": [1],
              "times": ["09:30"],
              "duration": 60,
              "durationUnit": "minutes"
            }
          }
        ]
      },
      {
        suggestedBy: 'Prof B',
        "requestedBy": null,
        status: "Pending",
        submittedOn: moment('24 Mar 2019 11:34:00').format('MMMM D YYYY (dddd) h:mm:ss a'),
        locationConflict: false,
        classConflict: true,
        professorConflict: false,
        conflict: [
          {
            "data": {
              "courseName": "50.003 Elements of Software Constructions",
              "pillar": "ISTD",
              "id": "001",
              "title": "50.003 Tutorial",
              "color": "#9C27B0",
              "location": "2.501",
              "professor": "Sun Jun",
              "classEnrolled": "F01",
              "calendarType": "Academic",
              "locked": null,
              "suggestedBy": null,
              "requestedBy": null,
              "isSelected": false
            },
            "schedule": {
              "dayOfWeek": [2],
              "times": ["10:00"],
              "duration": 60,
              "durationUnit": "minutes"
            }
          },
          {
            "data": {
              "courseName": "50.003 Elements of Software Constructions",
              "pillar": "ISTD",
              "id": "002",
              "title": "50.005 Tutorial",
              "color": "#1976d2",
              "location": "2.507",
              "professor": "Gemma Roig",
              "classEnrolled": "F01",
              "calendarType": "Academic",
              "locked": null,
              "suggestedBy": "Prof B",
              "requestedBy": null,
              "isSelected": false
            },
            "schedule": {
              "dayOfWeek": [2],
              "times": ["10:30"],
              "duration": 60,
              "durationUnit": "minutes"
            }
          }
        ]
      }
    ]
  }),
  components: {
    AppHeader,
    SearchBar,
    // WeeklyCalendar,
    // dsWeeklyCalendar,
    FormSubmit,
    FinalisedCalendar,
    SuggestibleCalendar,
    RequestableCalendar,
    ApproveTable,
    ViewStatusTable
  },
  computed: {
    //TO CHANGE: get from database (main table)
    //main database table
    calendarEventTable(){

      // console.log(new Day(this.$termStartDate.clone().day("Monday").add(6, 'weeks')).date);
      // console.log(this.$termStartDate.clone().day("Monday").add(6, 'weeks').format());
      // console.log(this.$termStartDate.format());
      return [
        {
        "data": {
          "courseName": "50.003 Elements of Software Constructions",
          "pillar": "ISTD",
          "id": "001",
          "title": "50.003 Tutorial",
          "color": null,
          "location": "2.501",
          "professor": "Sun Jun",
          "classEnrolled": "F01",
          "calendarType": "Academic",
          "readonly": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [1],
          "times": ["09:00"],
          "duration": 60,
          "durationUnit": "minutes",
          "exclude": [this.$termStartDate.clone().day(2).add(6, 'weeks').format('YYYYMMDD').concat("0900")],
          "start": this.$termStartDate,
          "end": this.$termEndDate
        }
      },
      {
        "data": {
          "courseName": "50.003 Elements of Software Constructions",
          "pillar": "ISTD",
          "id": "002",
          "title": "50.003 Lecture",
          "color": null,
          "location": "1.203",
          "professor": "Sun Jun",
          "classEnrolled": "F01",
          "calendarType": "Academic",
          "readonly": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [2],
          "times": ["10:00"],
          "duration": 90,
          "durationUnit": "minutes",
          "exclude": [this.$termStartDate.clone().day(2).add(6, 'weeks').format('YYYYMMDD').concat("1000")],
          "start": this.$termStartDate,
          "end": this.$termEndDate
        }
      },
      {
        "data": {
          "courseName": "50.005 Computer Systems Engineering",
          "pillar": "ESD",
          "id": "003",
          "title": "50.005 Lab",
          "color": "#9C26B0",
          "location": "2.501",
          "professor": "Sun Jun",
          "classEnrolled": "F01",
          "calendarType": "Academic",
          "readonly": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [1],
          "times": ["14:00"],
          "duration": 60,
          "durationUnit": "minutes",
          "exclude": [this.$termStartDate.clone().day(1).add(6, 'weeks').format('YYYYMMDD').concat("1400")],
          "start": this.$termStartDate,
          "end": this.$termEndDate
        }
      },
      {
        "data": {
          "courseName": "50.005 Computer Systems Engineering",
          "pillar": "ESD",
          "id": "004",
          "title": "50.005 Lecture",
          "color": "#9C26B0",
          "location": "1.203",
          "professor": "Sudipta",
          "classEnrolled": "F01",
          "calendarType": "Academic",
          "readonly": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [4],
          "times": ["11:00"],
          "duration": 90,
          "durationUnit": "minutes",
          "exclude": [this.$termStartDate.clone().day(4).add(6, 'weeks').format('YYYYMMDD').concat("1100")],
          "start": this.$termStartDate,
          "end": this.$termEndDate
        }
      },
      {
        "data": {
          "courseName": "50.034 Probability and Statistics",
          "pillar": "EPD",
          "id": "005",
          "title": "50.034 Tutorial",
          "color": "#3F51B5",
          "location": "2.501",
          "professor": "Sun Jun",
          "classEnrolled": "F01",
          "calendarType": "Academic",
          "readonly": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [1],
          "times": ["09:00"],
          "duration": 60,
          "durationUnit": "minutes",
          "exclude": [this.$termStartDate.clone().day(1).add(6, 'weeks').format('YYYYMMDD').concat("0900")],
          "start": this.$termStartDate,
          "end": this.$termEndDate
        }
      },
      {
        "data": {
          "courseName": "50.034 Probability and Statistics",
          "pillar": "EPD",
          "id": "006",
          "title": "50.034 Lecture",
          "color": "#3F51B5",
          "location": "1.203",
          "professor": "Sun Jun",
          "classEnrolled": "F01",
          "calendarType": "Academic",
          "readonly": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [2],
          "times": ["10:00"],
          "duration": 90,
          "durationUnit": "minutes",
          "exclude": [this.$termStartDate.clone().day(2).add(6, 'weeks').format('YYYYMMDD').concat("1000")],
          "start": this.$termStartDate,
          "end": this.$termEndDate
        }
      },
      {
        "data": {
          "courseName": "50.004 Algorithms",
          "pillar": "ASD",
          "id": "006",
          "title": "50.004 Tutorial",
          "color": "#E91E63",
          "location": "2.501",
          "professor": "Sun Jun",
          "classEnrolled": "F01",
          "calendarType": "Academic",
          "readonly": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [1],
          "times": ["09:00"],
          "duration": 60,
          "durationUnit": "minutes",
          "exclude": [this.$termStartDate.clone().day(1).add(6, 'weeks').format('YYYYMMDD').concat("0900")],
          "start": this.$termStartDate,
          "end": this.$termEndDate
        }
      },
      {
        "data": {
          "courseName": "50.004 Algorithms",
          "pillar": "ASD",
          "id": "008",
          "title": "50.004 Lecture",
          "color": "#E91E63",
          "location": "1.203",
          "professor": "Sun Jun",
          "classEnrolled": "F01",
          "calendarType": "Academic",
          "readonly": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [2],
          "times": ["10:00"],
          "duration": 90,
          "durationUnit": "minutes",
          "exclude": [this.$termStartDate.clone().day(2).add(6, 'weeks').format('YYYYMMDD').concat("1000")],
          "start": this.$termStartDate,
          "end": this.$termEndDate
        }
      },
      {
        "data": {
          "courseName": "01.112 Machine Learning",
          "pillar": "FRESHMORE",
          "id": "009",
          "title": "01.112 Tutorial",
          "color": "#FFEB3B",
          "location": "2.501",
          "professor": "Sun Jun",
          "classEnrolled": "F01",
          "calendarType": "Academic",
          "readonly": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [1],
          "times": ["09:00"],
          "duration": 60,
          "durationUnit": "minutes",
          "exclude": [this.$termStartDate.clone().day(1).add(6, 'weeks').format('YYYYMMDD').concat("0900")],
          "start": this.$termStartDate,
          "end": this.$termEndDate
        }
      },
      {
        "data": {
          "courseName": "01.112 Machine Learning",
          "pillar": "FRESHMORE",
          "id": "010",
          "title": "01.112 Lecture",
          "color": "#FFEB3B",
          "location": "1.203",
          "professor": "Sun Jun",
          "classEnrolled": "F01",
          "calendarType": "Academic",
          "readonly": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [2],
          "times": ["10:00"],
          "duration": 90,
          "durationUnit": "minutes",
          "exclude": [this.$termStartDate.clone().day(2).add(6, 'weeks').format('YYYYMMDD').concat("1000")],
          "start": this.$termStartDate,
          "end": this.$termEndDate
        }
      },
      {
        "data": {
          "courseName": "50.040 Natural Language Processing",
          "pillar": "HASS",
          "id": "011",
          "title": "50.040 Tutorial",
          "color": "#2196F3",
          "location": "2.501",
          "professor": "Sun Jun",
          "classEnrolled": "F01",
          "calendarType": "Academic",
          "readonly": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [1],
          "times": ["09:00"],
          "duration": 60,
          "durationUnit": "minutes",
          "exclude": [this.$termStartDate.clone().day(1).add(6, 'weeks').format('YYYYMMDD').concat("0900")],
          "start": this.$termStartDate,
          "end": this.$termEndDate
        }
      },
      {
        "data": {
          "courseName": "50.040 Natural Language Processing",
          "pillar": "HASS",
          "id": "012",
          "title": "50.040 Lecture",
          "color": "#2196F3",
          "location": "1.203",
          "professor": "Sun Jun",
          "classEnrolled": "F01",
          "calendarType": "Academic",
          "readonly": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [2],
          "times": ["10:00"],
          "duration": 90,
          "durationUnit": "minutes",
          "exclude": [this.$termStartDate.clone().day(2).add(6, 'weeks').format('YYYYMMDD').concat("1000")],
          "start": this.$termStartDate,
          "end": this.$termEndDate
        }
      },
      {
        "data": {
          "courseName": "50.006 User Interface",
          "pillar": "ISTD",
          "id": "013",
          "title": "50.006 Tutorial",
          "color": "#2196F3",
          "location": "2.501",
          "professor": "Sun Jun",
          "classEnrolled": "F01",
          "calendarType": "Academic",
          "readonly": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [1],
          "times": ["09:00"],
          "duration": 60,
          "durationUnit": "minutes",
          "exclude": [this.$termStartDate.clone().day(1).add(6, 'weeks').format('YYYYMMDD').concat("0900")],
          "start": this.$termStartDate,
          "end": this.$termEndDate
        }
      },
      {
        "data": {
          "courseName": "50.006 User Interface",
          "pillar": "ISTD",
          "id": "014",
          "title": "50.006 Lecture",
          "color": "#2196F3",
          "location": "1.203",
          "professor": "Sun Jun",
          "classEnrolled": "F01",
          "calendarType": "Academic",
          "readonly": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [2],
          "times": ["10:00"],
          "duration": 90,
          "durationUnit": "minutes",
          "exclude": [this.$termStartDate.clone().day(2).add(6, 'weeks').format('YYYYMMDD').concat("1000")],
          "start": this.$termStartDate,
          "end": this.$termEndDate
        }
      }
    ]},
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
  },
  created() {
    this.$eventHub.$on('event-update', this.updateModifiable);
    this.$eventHub.$on('save-state', this.saveState)
    this.loadState();
  },
  beforeDestroy() {
    this.$eventHub.$off('event-update');
    this.$eventHub.$off('save-state');
  },
  methods: {
    toggleVisible : function(item) {
      this.activeComp.formSubmitNewCourse = false;
      this.activeComp.viewCurrSuggestions = false;
      this.activeComp.exportCoursesForPlanner = false;
      this.activeComp.viewTimetableToSuggest = false;
      this.activeComp.viewFinalTimetable = false;
      this.activeComp.viewExistingRequests = false;
      this.activeComp.requestChangesToCalendar = false;
      //this.activeComp.courseListingForViewer = false;
      this.activeComp.viewSuggestions = false;

      if(item == "formSubmitNewCourse"){
        this.activeComp.formSubmitNewCourse = true;
      }
      if(item == "viewCurrSuggestions"){
        this.activeComp.viewCurrSuggestions = true;
      }
      if(item == "exportCoursesForPlanner"){
        this.activeComp.exportCoursesForPlanner = true;
      }
      if(item == "viewTimetableToSuggest"){
        // this.modifiableCalendarEvent = {locked:[], modifiable: []};
        this.activeComp.viewTimetableToSuggest = true
      }
      if(item == "viewExistingRequests"){
        this.activeComp.viewExistingRequests = true;
      }
      if(item == "requestChangesToCalendar"){
        // this.modifiableCalendarEvent = {locked:[], modifiable: []};
        this.activeComp.requestChangesToCalendar = true;
      }
      // if(item == "courseListingForViewer"){
      //   this.activeComp.courseListingForViewer = true;
      // }
      if(item == "viewFinalTimetable"){
        this.activeComp.viewFinalTimetable = true;
      }
      if(item == "viewSuggestions"){
        this.activeComp.viewSuggestions = true;
      }
    },
    getColour(){
      let colour = Colors[Math.floor(Colors.length * Math.random())].value;
      while (this.coloursUsed.length < Colors.length && this.coloursUsed.includes(colour)){
        this.getColour();
      }
      //if colour is black or grey
      while (colour === "#000000" || colour === '#9E9E9E'){
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
          if (e.isSelected){
            if (!this.coloursMap.get(e.item)) {
              const colour = this.getColour();
              this.coloursMap.set(e.item, colour);
            }
            lesson.data.color = this.coloursMap.get(e.item);
          }
          //updating modifiable calendar
          if (e.isSelected === true && lesson.data.calendarType === 'Academic'){
            var modifiableEvent = JSON.parse(JSON.stringify(lesson)) //copying event object
            modifiableEvent.data.readonly = false;
            modifiableEvent.data.suggestedBy = this.username;
            modifiableEvent.data.requestedBy = this.username; 
            this.modifiableCalendarEvent.modifiable.push(modifiableEvent);
            var lockedEvent = JSON.parse(JSON.stringify(lesson)); //copying event object
            lockedEvent.data.readonly = true;
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
        event.data.readonly = false;
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
    },
    updateConflicts(item){
      this.possibleConflictingEvents = [];
      if (item.locationConflict){
        for (var lessonLocation of this.calendarEventTable){
        //TO CHANGE: hardcoding change--to change in database
          const location = item.conflict[0].data.location;
          outer_block:{
            if (lessonLocation.data.location === location){
              for (var conflictLessonLocation of item.conflict){
                if (conflictLessonLocation.data.id === lessonLocation.data.id){
                  break outer_block;  //continue checking other lessons
                }
              }      
              this.possibleConflictingEvents.push(lessonLocation);
            }
          }
        }
      }
      if (item.classConflict){
        //TO CHANGE: hardcoding change--to change in database
        for (var lessonClass of this.calendarEventTable){
          const classEnrolled = item.conflict[0].data.classEnrolled;
          outer_block:{
            if (lessonClass.data.classEnrolled === classEnrolled){
              for (var conflictLessonClass of item.conflict){
                if (conflictLessonClass.data.id === lessonClass.data.id){
                  break outer_block;  //continue checking other lessons
                }
              }     
              this.possibleConflictingEvents.push(lessonClass);
            }
          }
        }
      }
      if (this.professorConflict){
        //TO CHANGE: hardcoding change--to change in database
        for (var lessonProf of this.calendarEventTable){
          const professor = item.conflict[0].data.professor;
          outer_block:{
            if (lessonProf.data.professor === professor){
              for (var conflictLessonProf of item.conflict){
                if (conflictLessonProf.data.id === lessonProf.data.id){
                  break outer_block;  //continue checking other lessons
                }
              }      
              this.possibleConflictingEvents.push(lessonProf);
            }
          }
        }
      }
    },
    //TO CHANGE: check for conflict and update database
    updateSuggested(calendar){
      this.suggestibleTable.push({
        suggestedBy: this.username,
        calendar: calendar,
        submittedOn:  moment().format('MMMM D YYYY (dddd) h:mm:ss a'),
        status: "Pending",
        locationConflict: false,
        classConflict: true,
        professorConflict: false,
        conflict: this.conflicts
      })
      this.conflicts = [];
    },
    updateRequested(calendar){
      this.requestableTable.push({
        requestedBy: this.username,
        calendar: calendar,
        submittedOn:  moment().format('MMMM D YYYY (dddd) h:mm:ss a'),
        status: "Pending",
        locationConflict: false,
        classConflict: true,
        professorConflict: false,
        conflict: this.conflicts
      })
      this.conflicts = [];
    }
  },
  // hasLocationConflict(calendar){
  //   let events = JSON.parse(calendar).events;
  //   for (var event of events){
  //     for (var lesson of this.calendarEventTable){
  //       if (lesson.schedule.dayOfWeek[0] === event.schedule.dayOfWeek[0])
  //         if (lesson.schedule.times[0] === event.schedule.times[0]){
  //           if (lesson.data.location === event.schedule.location){
  //             if (this.conflits.length === 0){
  //               this.conflicts.push(event);
  //             }
  //             this.conflicts.push(lesson);
  //             return true;
  //           }
  //       }
  //     }
  //   }
  //   return false;
  // },
  // hasClassConflict(calendar){
  //   let events = JSON.parse(calendar).events;
  //   for (var event of events){
  //     for (var lesson of this.calendarEventTable){
  //       if (lesson.schedule.dayOfWeek[0] === event.schedule.dayOfWeek[0])
  //         if (lesson.schedule.times[0] === event.schedule.times[0]){
  //           if (lesson.data.classEnrolled === event.schedule.classEnrolled){
  //             if (this.conflits.length === 0){
  //               this.conflicts.push(event);
  //             }
  //             this.conflicts.push(lesson);
  //             return true;
  //           }
  //       }
  //     }
  //   }
  //   return false;
  // },
  // hasProfessorConflict(calendar){
  //   let events = JSON.parse(calendar).events;
  //   for (var event of events){
  //     for (var lesson of this.calendarEventTable){
  //       if (lesson.schedule.dayOfWeek[0] === event.schedule.dayOfWeek[0])
  //         if (lesson.schedule.times[0] === event.schedule.times[0]){
  //           if (lesson.data.professor === event.schedule.professor){
  //             if (this.conflits.length === 0){
  //               this.conflicts.push(event);
  //             }
  //             this.conflicts.push(lesson);
  //             return true;
  //           }
  //       }
  //     }
  //   }
  //   return false;
  // },
  saveState(){
    console.log("saving...");
    let suggestible = this.suggestibleTable;
    let jsonSuggestible = JSON.stringify(suggestible);
    localStorage.setItem('suggestibleTable', jsonSuggestible);

    let requestable = this.requestableTable;
    let jsonRequestable = JSON.stringify(requestable);
    localStorage.setItem('requestableTable', jsonRequestable);
  },
  loadState(){
    let state = {};
    try
    {
      let savedStateSuggestible = JSON.parse(localStorage.getItem('suggestibleTable'));
      let savedStateRequestable = JSON.parse(localStorage.getItem('requestableTable'));
      if (savedStateSuggestible)
      {
        this.suggestibleTable.concat(savedStateSuggestible);
      }
      if (savedStateRequestable)
      {
        this.requestableTable.concat(savedStateRequestable);
      }
    }
    catch (e)
    {
      console.log( e );
    }
  }
}
</script>  