<template>
  <div>
  <v-layout>
    <v-flex>
      <v-sheet height="400">
        <v-calendar
          ref="calendar"
          type="week"
        >
          <template v-slot:dayBody="{ date, timeToY, minutesToPixels }">
            <template v-for="event in eventsMap[date]">
            <v-menu 
              offset-x
              :key="event.title">
              <template v-slot:activator="{ on }">
                <div
                v-on="on"
                v-if="event.time"
                v-bind:key="event.title"
                :style="{ top: timeToY(event.time) + 'px', height: minutesToPixels(event.duration) + 'px' }"
                class="my-event with-time"
                v-html="event.title"
                ></div>
            </template>
            <v-card
                color="grey lighten-4"
                min-width="350px"
                flat
                >
                  <v-toolbar
                    color="primary"
                    dark
                  >
                    <v-btn icon>
                      <v-icon>edit</v-icon>
                    </v-btn>
                    <v-toolbar-title>{{ event.title }}</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn icon>
                      <v-icon>more_vert</v-icon>
                    </v-btn>
                  </v-toolbar>
                  <v-card-title primary-title>
                    <p>Start Time: {{ event.time }}</p>
                    <p>Location: {{ event.location }}</p>
                  </v-card-title>
                  <v-card-actions>
                    <v-btn
                      flat
                      color="secondary"
                    >
                      Cancel
                    </v-btn>
                  </v-card-actions>
                </v-card>
                </v-menu>
            </template>
          </template>
        </v-calendar>
      </v-sheet>
    </v-flex>
  </v-layout>
  </div>
</template>


<script>
  export default {
    name: 'WeeklyCalendar',
    props: {
        courseList: {
        type: Array,
        required: true,
        active: true
        }
    },
    data: () => ({
      events: [
        {
          title: 'Weekly Meeting',
          date: '2019-03-21',
          time: '09:00',
          duration: 45
        },
        {
          title: 'Thomas\' Birthday',
          date: '2019-01-10'
        },
        {
          title: 'Mash Potatoes',
          date: '2019-03-22',
          time: '12:30',
          duration: 180
        }
      ]
    }),
    computed: {
      // convert the list of events into a map of lists keyed by date
      eventsMap () {
        const map = {}
        for (var course of this.coursesSelected){
          course.lessonTimes.forEach(e => (map[e.date] = map[e.date] || []).push(e))
        }
        return map
      },
      coursesSelected: {
        get: function() {
          return this.courseList.filter(course => course.isSelected);
        },
        set: function(courses) {
          for (var course of this.courseList){
            this.remove(course);
          }
          for (var courseSelected of courses){
            courseSelected.isSelected = true;
          }
        }
      }
    },
    mounted () {
      this.$refs.calendar.scrollToTime('08:00')     
    },
    methods: {
      open (event) {
        alert(event.title)
      }
    }
  }
</script>


<style lang="stylus" scoped>
  .my-event {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    border-radius: 2px;
    background-color: #1867c0;
    color: #ffffff;
    border: 1px solid #1867c0;
    font-size: 12px;
    padding: 3px;
    cursor: pointer;
    margin-bottom: 1px;
    left: 4px;
    margin-right: 8px;
    position: relative;

    &.with-time {
      position: absolute;
      right: 4px;
      margin-right: 0px;
    }
  }
</style>