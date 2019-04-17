<template>
  <app-calendar
    :events="events"
    username="Guest"
    mode="finalised"   
  >
  </app-calendar>
</template>

<script>
import { Calendar } from 'dayspan';
import AppCalendar from '../components/AppCalendar.vue';

export default {
    name: 'FinalisedCalendar',
    props: {
      events: {
        type: Array
      },
      calendar: {
        type: Calendar
      }
    },
    components: {
      AppCalendar
    },
    data: vm => ({
    })
}
</script>
