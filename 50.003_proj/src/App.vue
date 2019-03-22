<template>
  <div>
    <v-app id="inspire">
      <app-header></app-header>
      <search-courses :courseList="courseList"></search-courses>
      <list-selection :courseList="courseList"></list-selection>
      <weekly-calendar :courseList="courseList"></weekly-calendar>
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
          "isSelected": true,
          'lessonTimes': [ 
            {
              title: '50.003 Tutorial',
              date: '2019-03-21',
              time: '09:00',
              duration: 60,
              location: '2.501'
            },
            {
              title: '50.003 Lecture',
              date: '2019-03-19',
              time: '10:00',
              duration: 90,
              location: '1.203'
            }
          ]},
        {"courseName": "50.005 Computer Systems Engineering",
        "id": "50.005",
        "pillar": "ESD",
        "isSelected": true,
        'lessonTimes': [ 
            {
              title: '50.005 Lab',
              date: '2019-03-20',
              time: '14:00',
              duration: 60,
              location: '2.501'
            },
            {
              title: '50.005 Lecture',
              date: '2019-03-22',
              time: '11:00',
              duration: 90,
              location: '1.203'
            }
          ]},
        {"courseName": "50.034 Probability and Statistics",
        "id": "50.034",
        "pillar": "EPD",
        "isSelected": true,
        'lessonTimes': [ 
            {
              title: '50.003 Tutorial',
              date: '2019-03-21',
              time: '09:00',
              duration: 60,
              location: '2.501'
            },
            {
              title: '50.003 Lecture',
              date: '2019-03-19',
              time: '10:00',
              duration: 90,
              location: '1.203'
            }
          ]},
        {"courseName": "50.004 Algorithms",
        "id": "50.004",
        "pillar": "ASD",
        "isSelected": false,
        'lessonTimes': [ 
            {
              title: '50.003 Tutorial',
              date: '2019-03-21',
              time: '09:00',
              duration: 60,
              location: '2.501'
            },
            {
              title: '50.003 Lecture',
              date: '2019-03-19',
              time: '10:00',
              duration: 90,
              location: '1.203'
            }
          ]},
        {"courseName": "01.112 Machine Learning",
        "id": "01.112",
        "pillar": "FRESHMORE",
        "isSelected": false,
        'lessonTimes': [ 
            {
              title: '50.003 Tutorial',
              date: '2019-03-21',
              time: '09:00',
              duration: 60,
              location: '2.501'
            },
            {
              title: '50.003 Lecture',
              date: '2019-03-19',
              time: '10:00',
              duration: 90,
              location: '1.203'
            }
          ]},
        {"courseName": "50.040 Natural Language Processing",
        "id": "50.040",
        "pillar": "HASS",
        "isSelected": false,
        'lessonTimes': [ 
            {
              title: '50.003 Tutorial',
              date: '2019-03-21',
              time: '09:00',
              duration: 60,
              location: '2.501'
            },
            {
              title: '50.003 Lecture',
              date: '2019-03-19',
              time: '10:00',
              duration: 90,
              location: '1.203'
            }
          ]},
        {"courseName": "50.006 User Interface",
        "id": "50.006",
        "pillar": "ISTD",
        "isSelected": false,
        'lessonTimes': [ 
            {
              title: '50.003 Tutorial',
              date: '2019-03-21',
              time: '09:00',
              duration: 60,
              location: '2.501'
            },
            {
              title: '50.003 Lecture',
              date: '2019-03-19',
              time: '10:00',
              duration: 90,
              location: '1.203'
            }
          ]}
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