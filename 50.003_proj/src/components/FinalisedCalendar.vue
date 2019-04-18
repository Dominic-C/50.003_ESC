<template>
  <div>
    <slot name="header"></slot>
    <app-calendar
      :events="events"
      :calendar="calendar"
      username="Guest"
      mode="finalised"   
    >
    </app-calendar>
  </div>
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
