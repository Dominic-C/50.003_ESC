<template>
  <div>
    <v-app id="inspire">
      <app-header></app-header>
      <search-courses :courseList="courseList" :isActive="isActive"></search-courses>
      <list-selection :courseList="courseList" :isActive="isActive"></list-selection>
      <weekly-calendar :courseList="courseList" :isActive="isActive"></weekly-calendar>
    </v-app>
  </div>
</template>

<script>
import AppHeader from './components/AppHeader.vue';
import SearchCourses from './components/SearchCourses.vue';
import ListSelection from './components/ListSelection.vue';
import WeeklyCalendar from './components/WeeklyCalendar.vue';

export default {
  name: 'app',
  data: () => ({
    courseList: [
        {"courseName": "50.003 Elements of Software Constructions",
          "id": "50.003",
          "pillar": "ISTD",
          "isSelected": true},
        {"courseName": "50.005 Computer Systems Engineering",
        "id": "50.005",
        "pillar": "ESD",
        "isSelected": true},
        {"courseName": "50.034 Probability and Statistics",
        "id": "50.034",
        "pillar": "EPD",
        "isSelected": true},
        {"courseName": "50.004 Algorithms",
        "id": "50.004",
        "pillar": "ASD",
        "isSelected": false},
        {"courseName": "01.112 Machine Learning",
        "id": "01.112",
        "pillar": "FRESHMORE",
        "isSelected": false},
        {"courseName": "50.040 Natural Language Processing",
        "id": "50.040",
        "pillar": "HASS",
        "isSelected": false},
        {"courseName": "50.006 User Interface",
        "id": "50.006",
        "pillar": "ISTD",
        "isSelected": false}
      ],
    isActive: [
      {
        "name": "weeklyCalendar",
        "live": true
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
    WeeklyCalendar
  }
}
</script>  