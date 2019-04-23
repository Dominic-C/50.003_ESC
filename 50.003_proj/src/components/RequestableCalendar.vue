<template>
  <app-calendar
    :username="username"
    :events="currentEvents"
    :isInMode="isRequesting"
    :calendar="calendar"
    :dialog="dialog"
    mode="requestable"   
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
        @click="dialog = true"
      >
        Push Request
      </v-btn>
    </template>

    <!-- Status -->
    <template slot="status" slot-scope="{ details }">
      <v-text-field 
        single-line hide-details solo flat
        :prepend-icon="details.locked ? 'lock' : 'lock_open'"
        :label="details.locked ? 'Current Calendar' : 'Requested Change'"
        disabled
      ></v-text-field>
    </template>

    <!-- Requested by -->
    <template slot="additionalInfo" slot-scope="{ details }">
      <v-layout row>
        <v-flex xs2>
          <v-subheader v-if="details.requestedBy">Requested by</v-subheader>
        </v-flex>
        <v-flex xs10>
          <v-text-field 
            v-if="details.requestedBy"
            single-line hide-details solo flat
            disabled
            v-model="details.requestedBy"
          ></v-text-field>
        </v-flex>
      </v-layout>
    </template>

    <!-- confirm dialog -->
    <template slot="title">
      <v-card-title class="headline">Send request?</v-card-title>
    </template>
    <template slot="text">
      <v-card-text>
          Push the request you have made to database for the time table planner to review. 
          Requests cannot be edited once sent but can be cancelled.
        </v-card-text>
    </template>
    <template slot="noButton">
      <v-btn
					color="green darken-1"
					flat="flat"
					@click="dialog = false"
				>
					Cancel
				</v-btn>
    </template>
    <template slot="yesButton">
      <v-btn
        color="green darken-1"
        flat="flat"
        @click="pushToDatabase"
      >
        OK
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
      type: Calendar,
      default(){
        return Calendar.weeks();
      }
		}
  },
  components: {
    AppCalendar
  },
  data: () => ({
    storeKey: 'requestableCalendar',
    isRequesting: false,
    dialog: false
  }),
  computed: {
    currentEvents(){
      return this.events.locked.concat(this.events.modifiable);
    }    
  },
  methods: {
    revertState(){
      this.isRequesting = false;
      this.$emit('revert-state');
    },
    pushToDatabase(){
      //TO CHANGE: save to database eventually
      let state = this.calendar.toInput(true);
      let json = JSON.stringify(state);
      localStorage.setItem(this.storeKey, json);
      this.dialog = false;
      this.isRequesting = false;
      this.$emit('requested', json); //for testing
    }
  }  
}
</script>
