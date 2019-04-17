<template>
  <app-calendar
    :username="username"
    :events="currentEvents"
    :isInMode="isSuggesting"
    mode="suggestible"   
    ref="calendar" 
  >   
    <template slot="switchModeButton">
      <v-btn 
        color="primary"
        @click="isSuggesting=true"
      >
        Suggest Timings
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
        Push Suggestions
      </v-btn>
    </template>
  </app-calendar>
</template>

<script>
import { Calendar } from 'dayspan';
import AppCalendar from '../components/AppCalendar.vue'

export default {
  name: 'SuggestibleCalendar',
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
    storeKey: 'suggestableCalendar',
    isSuggesting: false
  }),
  computed: {
    currentEvents(){
      return this.events.locked.concat(this.events.modifiable);
    }    
  },
  methods: {
    revertState(){
      this.isSuggesting = false;
      this.$emit('revert-state');
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
