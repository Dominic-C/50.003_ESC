<template>
  <app-calendar
    :username="username"
    :events="events"
    :isInMode="isBooking"
    :calendar="calendar"
    :dialog="dialog"
    mode="bookable"   
    ref="calendar" 
  >   
    <template slot="switchModeButton">
      <v-btn 
        color="primary"
        @click="isBooking=true"
      >
        Book Event
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
        Push Booking
      </v-btn>
    </template>

    <!-- Booked by -->
    <template slot="additionalInfo" slot-scope="{ details }">
      <v-layout row>
        <v-flex xs2>
          <v-subheader v-if="details.bookedBy">Booked by</v-subheader>
        </v-flex>
        <v-flex xs10>
          <v-text-field 
            v-if="details.bookedBy"
            single-line hide-details solo flat
            disabled
            v-model="details.bookedBy"
          ></v-text-field>
        </v-flex>
      </v-layout>
    </template>

    <!-- confirm dialog -->
    <template slot="title">
      <v-card-title class="headline">Book event?</v-card-title>
    </template>
    <template slot="text">
      <v-card-text>
				Push the booking you have made to database. 
				Bookings are added to the finalised timetable and is visible to all.
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
  name: 'BookableCalendar',
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
    storeKey: 'bookableCalendar',
    isBooking: false,
    dialog: false
  }),
  computed: {
    currentEvents(){
      return this.events.locked.concat(this.events.modifiable);
    }    
  },
  methods: {
    revertState(){
      this.isBooking = false;
      this.$emit('revert-state');
    },
    pushToDatabase(){
      //TO CHANGE: save to database eventually
      let state = this.calendar.toInput(true);
      let json = JSON.stringify(state);
      localStorage.setItem(this.storeKey, json);
      this.dialog = false;
      this.isBooking = false;
      this.$emit('booked', json); //for testing
    }
  }  
}
</script>
