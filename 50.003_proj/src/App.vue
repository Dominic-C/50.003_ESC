<template>
  <div id="app">
    <v-app id="dayspan" v-cloak>
      <app-header @changeComp="toggleVisible"></app-header>
      <v-content>
        <form-submit v-if="activeComp.formSubmitNewCourse"></form-submit>
        <search-bar 
          :calendarEventsTable="calendarEventTable"
          :professorTable="professorTable"
          :courseNameTable="courseNameTable"
          :locationTable="locationTable"
          :classTable="classTable"
          @selected-search-item="updateCalendar"
          v-if="activeComp.courseListingForViewer || activeComp.viewTimetableToSuggest || activeComp.viewFinalTimetable || activeComp.requestChangesToCalendar">
        </search-bar>
        <!-- <list-selection :courseList="courseTable" v-if="activeComp.courseListingForViewer"></list-selection> -->
        <!-- <weekly-calendar :courseList="courseList" v-if="false"></weekly-calendar> -->
        <finalised-calendar :events="selectedCalendarEvents" v-if="activeComp.viewFinalTimetable">></finalised-calendar>
        <suggestible-calendar ref='suggestCalendar'
          :events="modifiableCalendarEvent"
          :username="username"
          @revert-state="revertState"
          v-if="activeComp.viewTimetableToSuggest"></suggestible-calendar>
        <requestable-calendar ref='requestCalendar'
          :events="modifiableCalendarEvent"
          :username="username"
          @revert-state="revertState"
          v-if="activeComp.requestChangesToCalendar"></requestable-calendar>
        <view-results-table  v-if="activeComp.viewSuggestions"></view-results-table>
      </v-content>
    </v-app>
  </div>
</template>

<script>
import { Weekday } from 'dayspan';
import Colors from 'dayspan-vuetify/src/colors.js';
import AppHeader from './components/AppHeader.vue';
import SearchBar from './components/SearchBar.vue';
import ListSelection from './components/ListSelection.vue';
// import WeeklyCalendar from './components/WeeklyCalendar.vue';
// import dsWeeklyCalendar from './components/DaySpanWeeklyCalendar.vue';
import FinalisedCalendar from './components/FinalisedCalendar.vue'
import SuggestibleCalendar from './components/SuggestibleCalendar.vue'
import RequestableCalendar from "./components/RequestableCalendar.vue";
import ViewResultsTable from "./components/ViewResultsTable";
import FormSubmit from './components/FormSubmit.vue';

export default {
  name: 'app',
  data: () => ({
    coloursUsed: [],
    modifiableCalendarEvent: {locked:[], modifiable:[]},
    username: "username", //TO CHANGE: replace with username
    //TO CHANGE: get from database (main table)
    //main database table
    calendarEventTable: [
      {
        "data": {
          "courseName": "50.003 Elements of Software Constructions",
          "pillar": "ISTD",
          "id": "001",
          "title": "50.003 Tutorial",
          "color": "#1976d2",
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
          "title": "50.003 Lecture",
          "color": "#1976d2",
          "location": "1.203",
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
          "duration": 90,
          "durationUnit": "minutes"
        }
      },
      {
        "data": {
          "courseName": "50.005 Computer Systems Engineering",
          "pillar": "ESD",
          "id": "003",
          "title": "50.005 Lab",
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
          "dayOfWeek": [1],
          "times": ["14:00"],
          "duration": 60,
          "durationUnit": "minutes"
        }
      },
      {
        "data": {
          "courseName": "50.005 Computer Systems Engineering",
          "pillar": "ESD",
          "id": "004",
          "title": "50.005 Lecture",
          "color": "#9C27B0",
          "location": "1.203",
          "professor": "Sudipta",
          "classEnrolled": "F01",
          "calendarType": "Academic",
          "locked": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [4],
          "times": ["11:00"],
          "duration": 90,
          "durationUnit": "minutes"
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
          "locked": null,
          "suggestedBy": null,
          "requestedBy": null,
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
          "courseName": "50.034 Probability and Statistics",
          "pillar": "EPD",
          "id": "006",
          "title": "50.034 Lecture",
          "color": "#3F51B5",
          "location": "1.203",
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
          "duration": 90,
          "durationUnit": "minutes"
        }
      },
      {
        "data": {
          "courseName": "50.004 Algorithms",
          "pillar": "ASD",
          "id": "007",
          "title": "50.004 Tutorial",
          "color": "#E91E63",
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
          "dayOfWeek": [1],
          "times": ["09:00"],
          "duration": 60,
          "durationUnit": "minutes"
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
          "locked": null,
          "suggestedBy": null,
          "requestedBy": null,
          "isSelected": false
        },
        "schedule": {
          "dayOfWeek": [2],
          "times": ["10:00"],
          "duration": 90,
          "durationUnit": "minutes"
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
          "locked": null,
          "suggestedBy": null,
          "requestedBy": null,
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
          "courseName": "01.112 Machine Learning",
          "pillar": "FRESHMORE",
          "id": "010",
          "title": "01.112 Lecture",
          "color": "#FFEB3B",
          "location": "1.203",
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
          "duration": 90,
          "durationUnit": "minutes"
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
          "locked": null,
          "suggestedBy": null,
          "requestedBy": null,
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
          "courseName": "50.040 Natural Language Processing",
          "pillar": "HASS",
          "id": "012",
          "title": "50.040 Lecture",
          "color": "#2196F3",
          "location": "1.203",
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
          "duration": 90,
          "durationUnit": "minutes"
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
          "locked": null,
          "suggestedBy": null,
          "requestedBy": null,
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
          "courseName": "50.006 User Interface",
          "pillar": "ISTD",
          "id": "014",
          "title": "50.006 Lecture",
          "color": "#2196F3",
          "location": "1.203",
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
          "duration": 90,
          "durationUnit": "minutes"
        }
      }
    ],
    courseTable: [
        {"courseName": "50.003 Elements of Software Constructions",
          "id": "50.003",
          "pillar": "ISTD",
          colour: '',
          'lessonTimes': [ 
            {
              title: '50.003 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
              classEnrolled: 'F01',
              professor: 'Sun Jun',
              "isSelected": false              
            },
            {
              title: '50.003 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203',
              classEnrolled: 'F01',
              professor: 'Sun Jun',
              "isSelected": false
            }
          ]},
        {"courseName": "50.005 Computer Systems Engineering",
        "id": "50.005",
        "pillar": "ESD",
        colour: '',
        'lessonTimes': [ 
            {
              title: '50.005 Lab',
              day: Weekday.MONDAY,
              time: '14:00',
              duration: 60,
              location: '2.501',
              classEnrolled: 'F01',
              professor: 'Sun Jun',
              "isSelected": false
            },
            {
              title: '50.005 Lecture',
              day: Weekday.THURSDAY,
              time: '11:00',
              duration: 90,
              location: '1.203',
              classEnrolled: 'F01',
              professor: 'Sudipta',
              "isSelected": false
            }
          ]},
        {"courseName": "50.034 Probability and Statistics",
        "id": "50.034",
        "pillar": "EPD",
        colour: '',
        'lessonTimes': [ 
            {
              title: '50.034 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
              classEnrolled: 'F01',
              professor: 'Sun Jun',
               "isSelected": false
            },
            {
              title: '50.034 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203',
              classEnrolled: 'F01',
              professor: 'Sun Jun',
              "isSelected": false
            }
          ]},
        {"courseName": "50.004 Algorithms",
        "id": "50.004",
        "pillar": "ASD",
        colour: '',
        'lessonTimes': [ 
            {
              title: '50.004 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
              classEnrolled: 'F01',
              professor: 'Sun Jun',
              "isSelected": false
              
            },
            {
              title: '50.004 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203',
              classEnrolled: 'F01',
              professor: 'Sun Jun',
              "isSelected": false
            }
          ]},
        {"courseName": "01.112 Machine Learning",
        "id": "01.112",
        "pillar": "FRESHMORE",
        colour: '',
        'lessonTimes': [ 
            {
              title: '01.112 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
              classEnrolled: 'F01',
              professor: 'Sun Jun',
              "isSelected": false
            },
            {
              title: '01.112 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203',
              classEnrolled: 'F01',
              professor: 'Sun Jun',
              "isSelected": false
            }
          ]},
        {"courseName": "50.040 Natural Language Processing",
        "id": "50.040",
        "pillar": "HASS",
        colour: '',
        'lessonTimes': [ 
            {
              title: '50.040 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
              classEnrolled: 'F01',
              professor: 'Sun Jun',
              "isSelected": false
            },
            {
              title: '50.040 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203',
              classEnrolled: 'F01',
              professor: 'Sun Jun',
              "isSelected": false
            }
          ]},
        {"courseName": "50.006 User Interface",
        "id": "50.006",
        "pillar": "ISTD",
        colour: '',
        'lessonTimes': [ 
            {
              title: '50.006 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
              classEnrolled: 'F01',
              professor: 'Sun Jun',
              "isSelected": false
            },
            {
              title: '50.006 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203',
              classEnrolled: 'F01',
              professor: 'Sun Jun',
              "isSelected": false
            }]
        }],
    activeComp: {
      // Submit new Course, Export Suggestions
      formSubmitNewCourse : false,
      viewCurrSuggestions : false,
      exportCoursesForPlanner : false,
      // Suggest new timings for course
      viewTimetableToSuggest : false,
      viewExistingRequests : false,
      // After Finalization activities:
      requestChangesToCalendar : false,
      courseListingForViewer : false,
      viewFinalTimetable : false
    }
  }),
  components: {
    AppHeader,
    SearchBar,
    ListSelection,
    // WeeklyCalendar,
    // dsWeeklyCalendar,
    FormSubmit,
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
  },
  created() {
    this.$eventHub.$on('event-update', this.updateModifiable);
  },
  beforeDestroy() {
      this.$eventHub.$off('event-update');
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
      this.activeComp.courseListingForViewer = false;
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
      if(item == "courseListingForViewer"){
        this.activeComp.courseListingForViewer = true;
      }
      if(item == "viewFinalTimetable"){
        this.activeComp.viewFinalTimetable = true;
      }
      if(item == "viewSuggestions"){
        this.activeComp.viewSuggestions = true;
      }
    },
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
}
</script>  