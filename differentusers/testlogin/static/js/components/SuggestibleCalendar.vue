<template>
  <modifiable-calendar
    :username="username"
    :events="currentEvents"
    :isInMode="isSuggesting"
    mode="suggestible"   
    @event-update="updateCalendar"
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
      >
        Push Suggestions
      </v-btn>
    </template>
  </modifiable-calendar>
</template>

<script>
import ModifiableCalendar from '../components/ModifiableCalendar.vue'

export default {
  name: 'SuggestibleCalendar',
  props: {
    events: {
      type: Object
    },
    username: {
      type: String,
      required: true
    }
  },
  components: {
    ModifiableCalendar
  },
  data: vm => ({
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
    updateCalendar(event){
      this.$emit('event-update', event);
    },
    applyEvents(){
      this.$refs.calendar.applyEvents();
    }
  }  
}
</script>
