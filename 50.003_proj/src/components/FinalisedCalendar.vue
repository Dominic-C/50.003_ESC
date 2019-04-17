<template>
  <app-calendar
    :events="events"
    mode="finalised"   
  >
  </app-calendar>
</template>

<script>
import { Calendar } from 'dayspan';
import AppCalendar from '../components/AppCalendar.vue'
export default {
    name: 'FinalisedCalendar',
    props: {
      events: {
        type: Array
      }
    },
    components: {
      AppCalendar
    },
    data: vm => ({
      calendar: Calendar.weeks()
    })
}
</script>
