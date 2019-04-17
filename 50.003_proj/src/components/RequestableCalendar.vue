<template>
  <app-calendar
    :username="username"
    :events="currentEvents"
    :isInMode="isRequesting"
    mode="requestable"   
    @event-update="updateCalendar"
    ref="calendar" 
  >   
    <template slot="switchModeButton">
      <v-btn 
        color="primary"
        @click="isRequesting=true"
      >
        Request Changes
      </v-btn>
    </template>
    <template slot="cancelButton">
      <v-btn 
        color="grey"
        @click="revertState"
      >
        Cancel
      </v-btn>
    </template>
    <template slot="pushButton">
      <v-btn 
        color="primary"
        @click="pushToDatabase"
      >
        Push Request
      </v-btn>
    </template>
  </app-calendar>
</template>

<script>
import { Calendar } from 'dayspan';
import AppCalendar from '../components/AppCalendar.vue'

export default {
  name: 'RequestableCalendar',
  props: {
    events: {
      type: Object
    },
    username: {
      type: String,
      required: true
    },
    calendar: {
			type: Calendar
		}
  },
  components: {
    AppCalendar
  },
  data: () => ({
    storeKey: 'requestableCalendar',
    isRequesting: false
  }),
  computed: {
    currentEvents(){
      return this.events.locked.concat(this.events.calendar);
    }    
  },
  methods: {
    revertState(){
      this.isRequesting = false;
      this.$emit('revert-state');
    },
    updateCalendar(event){
      this.$emit('event-update', event);
    },
    applyEvents(){
      this.$refs.calendar.applyEvents();
    },
    pushToDatabase(){
      //TO CHANGE: save to database eventually
      let state = this.calendar.toInput(true);
      let json = JSON.stringify(state);
      localStorage.setItem(this.storeKey, json);
    }
  }  
}
</script>
