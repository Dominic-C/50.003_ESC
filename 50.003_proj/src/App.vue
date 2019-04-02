<template>
  <div id="app">
    <v-app id="dayspan" v-cloak>
      <app-header @changeComp="toggleVisible"></app-header>
      <v-content>
        <form-submit v-if="activeComp.formSubmitNewCourse"></form-submit>
        <search-courses :courseList="courseList" v-if="activeComp.courseListingForViewer || activeComp.viewTimetableToSuggest"></search-courses>
        <list-selection :courseList="courseList" v-if="activeComp.courseListingForViewer"></list-selection>
        <!-- <weekly-calendar :courseList="courseList" v-if="false"></weekly-calendar> -->
        <weekly-calendar-finalised :events="calendarEvents" v-if="activeComp.viewTimetableToSuggest">></weekly-calendar-finalised>
        <weekly-calendar-suggestable :events="calendarEvents" v-if="activeComp.viewTimetableToSuggest">></weekly-calendar-suggestable>
        <!-- <ds-calendar :calendar="calendar" v-if="activeComp.weeklyCalendar">></ds-calendar> -->
        <!-- <v-app id="dayspan" v-cloak> -->
          <!-- <ds-calendar :calendar="calendar"></ds-calendar> -->
          <!-- <ds-weekly-calendar :events="calendarEvents"></ds-weekly-calendar> -->
        <!-- </v-app> -->
      </v-content>
    </v-app>
  </div>
</template>

<script>
import { Calendar, Weekday } from 'dayspan';
import Colors from 'dayspan-vuetify/src/colors.js';
import AppHeader from './components/AppHeader.vue';
import SearchCourses from './components/SearchCourses.vue';
import ListSelection from './components/ListSelection.vue';
import WeeklyCalendar from './components/WeeklyCalendar.vue';
import dsWeeklyCalendar from './components/DaySpanWeeklyCalendar.vue';
import weeklyCalendarFinalised from './components/WeeklyCalendarFinalised.vue'
import weeklyCalendarSuggestable from './components/WeeklyCalendarSuggestable.vue'
import FormSubmit from './components/FormSubmit.vue';

export default {
  name: 'app',
  data: () => ({
    calendar: Calendar.weeks(),
    coloursUsed: [],
    courseList: [
        {"courseName": "50.003 Elements of Software Constructions",
          "id": "50.003",
          "pillar": "ISTD",
          "isSelected": true,
          colour: '',
          'lessonTimes': [ 
            {
              title: '50.003 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
              classEnrolled: 'F01',
              professor: 'Sun Jun'              
            },
            {
              title: '50.003 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203',
              classEnrolled: 'F01',
              professor: 'Sun Jun'
            }
          ]},
        {"courseName": "50.005 Computer Systems Engineering",
        "id": "50.005",
        "pillar": "ESD",
        "isSelected": true,
        colour: '',
        'lessonTimes': [ 
            {
              title: '50.005 Lab',
              day: Weekday.MONDAY,
              time: '14:00',
              duration: 60,
              location: '2.501',
              classEnrolled: 'F01',
              professor: 'Sun Jun'
            },
            {
              title: '50.005 Lecture',
              day: Weekday.THURSDAY,
              time: '11:00',
              duration: 90,
              location: '1.203',
              classEnrolled: 'F01',
              professor: 'Sun Jun'
            }
          ]},
        {"courseName": "50.034 Probability and Statistics",
        "id": "50.034",
        "pillar": "EPD",
        "isSelected": true,
        colour: '',
        'lessonTimes': [ 
            {
              title: '50.034 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
              classEnrolled: 'F01',
              professor: 'Sun Jun'
            },
            {
              title: '50.034 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203',
              classEnrolled: 'F01',
              professor: 'Sun Jun',
            }
          ]},
        {"courseName": "50.004 Algorithms",
        "id": "50.004",
        "pillar": "ASD",
        "isSelected": false,
        colour: '',
        'lessonTimes': [ 
            {
              title: '50.004 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
              classEnrolled: 'F01',
              professor: 'Sun Jun'
              
            },
            {
              title: '50.004 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203',
              classEnrolled: 'F01',
              professor: 'Sun Jun'
            }
          ]},
        {"courseName": "01.112 Machine Learning",
        "id": "01.112",
        "pillar": "FRESHMORE",
        "isSelected": false,
        colour: '',
        'lessonTimes': [ 
            {
              title: '01.112 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
              classEnrolled: 'F01',
              professor: 'Sun Jun'
            },
            {
              title: '01.112 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203',
              classEnrolled: 'F01',
              professor: 'Sun Jun'
            }
          ]},
        {"courseName": "50.040 Natural Language Processing",
        "id": "50.040",
        "pillar": "HASS",
        "isSelected": false,
        colour: '',
        'lessonTimes': [ 
            {
              title: '50.040 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
              classEnrolled: 'F01',
              professor: 'Sun Jun'
            },
            {
              title: '50.040 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203',
              classEnrolled: 'F01',
              professor: 'Sun Jun'
            }
          ]},
        {"courseName": "50.006 User Interface",
        "id": "50.006",
        "pillar": "ISTD",
        "isSelected": false,
        colour: '',
        'lessonTimes': [ 
            {
              title: '50.006 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
              classEnrolled: 'F01',
              professor: 'Sun Jun'
            },
            {
              title: '50.006 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203',
              classEnrolled: 'F01',
              professor: 'Sun Jun'
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
      courseListingForViewer : false
    }
  }),
  components: {
    AppHeader,
    SearchCourses,
    ListSelection,
    WeeklyCalendar,
    dsWeeklyCalendar,
    FormSubmit,
    weeklyCalendarFinalised,
    weeklyCalendarSuggestable
  },
  computed: {
    calendarEvents() {
      var eventData = []
      for (var course of this.courseList){
        if (course.isSelected){
          for (var lesson of course.lessonTimes){
            eventData.push({
              data: {
                title: lesson.title,
                color: this.getColour(course),
                location: lesson.location,
                professor: lesson.professor,
                classEnrolled: lesson.classEnrolled,
                calendarType: "Academic",
                locked: null,
                suggestedBy: null,
                requestedBy: null
              },
              schedule: {
                dayOfWeek: [lesson.day],
                times: [lesson.time],
                duration: lesson.duration,
                durationUnit: 'minutes'
              }
            })
          }
        }
      }
      return eventData;  
    }
  },
  methods: {
    toggleVisible : function(item) {
      this.activeComp.formSubmitNewCourse = false
      this.activeComp.viewCurrSuggestions = false
      this.activeComp.exportCoursesForPlanner = false
      this.activeComp.viewTimetableToSuggest = false
      this.activeComp.viewExistingRequests = false
      this.activeComp.requestChangesToCalendar = false
      this.activeComp.courseListingForViewer = false

      if(item == "formSubmitNewCourse"){
        this.activeComp.formSubmitNewCourse = true
      }
      if(item == "viewCurrSuggestions"){
        this.activeComp.viewCurrSuggestions = true
      }
      if(item == "exportCoursesForPlanner"){
        this.activeComp.exportCoursesForPlanner = true
      }
      if(item == "viewTimetableToSuggest"){
        this.activeComp.viewTimetableToSuggest = true
      }
      if(item == "viewExistingRequests"){
        this.activeComp.viewExistingRequests = true
      }
      if(item == "requestChangesToCalendar"){
        this.activeComp.requestChangesToCalendar = true
      }
      if(item == "courseListingForViewer"){
        this.activeComp.courseListingForViewer = true
      }
    },
    getColour(course){
      if (course.colour === '') {
        let colour = Colors[Math.floor(Colors.length * Math.random())].value;
        if (this.coloursUsed.length < Colors.length && this.coloursUsed.includes(colour)){
          this.getColour();
        }
        this.coloursUsed.push(colour);
        course.colour = colour;
        return colour;
      } else {
        return course.colour;
      }
    }
  }
}
</script>  