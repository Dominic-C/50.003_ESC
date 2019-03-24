<template>
  <div>
    <v-app id="inspire">
      <app-header></app-header>
      <search-courses :courseList="courseList" :isActive="isActive"></search-courses>
      <list-selection :courseList="courseList" :isActive="isActive"></list-selection>
      <weekly-calendar :courseList="courseList" :isActive="isActive"></weekly-calendar>
      
      <v-app id="dayspan" v-cloak>
        <ds-weekly-calendar :events="calendarEvents"></ds-weekly-calendar>
        <!-- <calendar></calendar> -->
        <!-- <ds-calendar :calendar="calendar"></ds-calendar> -->
        <!-- <ds-calendar-app :calendar="calendar"></ds-calendar-app> -->
      </v-app>
  </v-app>
  </div>
</template>

<script>
import { Calendar, Weekday } from 'dayspan';
import AppHeader from './components/AppHeader.vue';
import SearchCourses from './components/SearchCourses.vue';
import ListSelection from './components/ListSelection.vue';
import WeeklyCalendar from './components/WeeklyCalendar.vue';
import dsWeeklyCalendar from './components/DaySpanWeeklyCalendar.vue';
// import Calendar from './components/Calendar.vue';

export default {
  name: 'app',
  data: () => ({
    calendar: Calendar.weeks(),
    courseList: [
        {"courseName": "50.003 Elements of Software Constructions",
          "id": "50.003",
          "pillar": "ISTD",
          "isSelected": true,
          "colour": '#2196F3',
          'lessonTimes': [ 
            {
              title: '50.003 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
            },
            {
              title: '50.003 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203'
            }
          ]},
        {"courseName": "50.005 Computer Systems Engineering",
        "id": "50.005",
        "pillar": "ESD",
        "isSelected": true,
        colour: '#2196F3',
        'lessonTimes': [ 
            {
              title: '50.005 Lab',
              day: Weekday.MONDAY,
              time: '14:00',
              duration: 60,
              location: '2.501',
            },
            {
              title: '50.005 Lecture',
              day: Weekday.THURSDAY,
              time: '11:00',
              duration: 90,
              location: '1.203'
            }
          ]},
        {"courseName": "50.034 Probability and Statistics",
        "id": "50.034",
        "pillar": "EPD",
        "isSelected": true,
        colour: '#2196F3',
        'lessonTimes': [ 
            {
              title: '50.034 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
            },
            {
              title: '50.034 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203'
            }
          ]},
        {"courseName": "50.004 Algorithms",
        "id": "50.004",
        "pillar": "ASD",
        "isSelected": false,
        colour: '#2196F3',
        'lessonTimes': [ 
            {
              title: '50.004 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
            },
            {
              title: '50.004 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203'
            }
          ]},
        {"courseName": "01.112 Machine Learning",
        "id": "01.112",
        "pillar": "FRESHMORE",
        "isSelected": false,
        colour: '#2196F3',
        'lessonTimes': [ 
            {
              title: '01.112 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
            },
            {
              title: '01.112 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203'
            }
          ]},
        {"courseName": "50.040 Natural Language Processing",
        "id": "50.040",
        "pillar": "HASS",
        "isSelected": false,
        colour: '#2196F3',
        'lessonTimes': [ 
            {
              title: '50.040 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
            },
            {
              title: '50.040 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203'
            }
          ]},
        {"courseName": "50.006 User Interface",
        "id": "50.006",
        "pillar": "ISTD",
        "isSelected": false,
        colour: '#2196F3',
        'lessonTimes': [ 
            {
              title: '50.006 Tutorial',
              day: Weekday.MONDAY,
              time: '09:00',
              duration: 60,
              location: '2.501',
            },
            {
              title: '50.006 Lecture',
              day: Weekday.TUESDAY,
              time: '10:00',
              duration: 90,
              location: '1.203'
            }]
        }],
    isActive: [
      {
        "name": "weeklyCalendar",
        "live": false
      },
      {
        "name": "searchCourses",
        "live": false
      }
    ]
  }),
  components: {
    AppHeader,
    SearchCourses,
    ListSelection,
    WeeklyCalendar,
    dsWeeklyCalendar,
    // Calendar
  },
  computed: {
    calendarEvents() {
      var eventData = []
      for (var course of this.courseList){
        if (course.isSelected){
          for (var lesson of course.lessonTimes)
          eventData.push({
            data: {
              title: lesson.title,
              color: course.colour
            },
            schedule: {
              schedule: {
                dayOfWeek: [lesson.day],
                times: [lesson.time],
                duration: lesson.duration,
                durationUnit: 'minutes'
              }
            }
          })
        }
      }   
    return eventData;
    }
  }
}
</script>  