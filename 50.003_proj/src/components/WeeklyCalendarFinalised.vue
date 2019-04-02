<template>
  <ds-weekly-calendar :events="events" :calendar="calendar" :read-only="readOnly">
    <template slot="eventDetailsExtra" slot-scope="{ details }">
      <v-text-field 
        single-line hide-details solo flat
        prepend-icon="school"
        label="Professor"
        disabled
        v-model="details.professor"
      >{{ details }}</v-text-field>
      <v-text-field 
        single-line hide-details solo flat
        prepend-icon="group"
        label="Class enrolled"
        :readonly="readOnly"
        v-model="details.classEnrolled"
      ></v-text-field>
    </template>
  </ds-weekly-calendar>
</template>

<script>
import { Calendar } from 'dayspan';
import dsWeeklyCalendar from '../components/DaySpanWeeklyCalendar.vue';
export default {
    name: 'weeklyCalendarFinalised',
    props: {
      events: {
        type: Array
      }
    },
    components: {
      dsWeeklyCalendar
    },
    data: vm => ({
      readOnly: true,
      calendar: Calendar.weeks()
    })
}
</script>
