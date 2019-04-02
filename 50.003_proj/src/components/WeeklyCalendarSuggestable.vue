<template>
  <ds-weekly-calendar :events="suggestibleEvents" :calendar="calendar" :read-only="false" :suggesting="true">
    <!-- <template slot="weeklyCalendar" slot-scope="{$scopedSlots, $listeners, calendar, add, addAt, edit, viewDay, handleAdd, handleMove}">
            <ds-weekly-calendar ref="calendar"
              v-bind="{$scopedSlots}"
              v-on="$listeners"
              :calendar="calendar"
              :read-only="false"
              @add="add"
              @add-at="addAt"
              @edit="edit"
              @view-day="viewDay"
              @added="handleAdd"
              @moved="handleMove"
              
            ></ds-weekly-calendar>
    </template> -->
  </ds-weekly-calendar>
</template>

<script>
import { Calendar } from 'dayspan';
import dsWeeklyCalendarSuggestable from '../components/DaySpanWeeklyCalendarSuggestable.vue';
import dsWeeklyCalendar from '../components/DaySpanWeeklyCalendar.vue';

export default {
  name: 'WeeklyCalendarSuggestable',
  props: {
    events: {
      type: Array
    },
    // labels:
    // {
    //   validate(x) {
    //     return this.$dsValidate(x, 'labels');
    //   },
    //   default() {
    //     return this.$dsDefaults().labels;
    //   }
    // }
  },
  components: {
    dsWeeklyCalendarSuggestable,
    dsWeeklyCalendar
  },
  data: vm => ({
    calendar: Calendar.weeks()
  }),
  computed: {
    suggestibleEvents(){
      var eventData = [];   
      for (var event of this.events){
        var lockedEvent = JSON.parse(JSON.stringify(event)) //copying event object
        var suggestingEvent = JSON.parse(JSON.stringify(event)) //copying event object
        // console.log(JSON.stringify(copyEvent.data));
        suggestingEvent.data.locked = false;
        lockedEvent.data.locked = true;
        lockedEvent.data.color = "#808080";
        eventData.push(lockedEvent);
        eventData.push(suggestingEvent);
      }
      // console.log(JSON.stringify(eventData[0].data));
      // console.log(this.events);
      return eventData;
    }    
  }
}
</script>
