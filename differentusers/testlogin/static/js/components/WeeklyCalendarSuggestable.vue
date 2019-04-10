<template>
  <div>
    <v-layout justify-end pb-3>
      <template v-if="!isSuggesting">
        <v-btn 
          color="primary"
          @click="isSuggesting=true"
        >
          Suggest Timings
        </v-btn>
      </template>
      <template v-else>
        <v-btn 
          color="grey"
          @click="revertState"
        >
          Cancel
        </v-btn>
        <v-btn color="primary">Push Suggestions</v-btn>
      </template>
    </v-layout>
    <div style="height: 500px">
      <ds-weekly-calendar 
        :events="suggestibleEvents" 
        :calendar="calendar" 
        :suggestable="true" 
        :read-only="!isSuggesting"
        @event-update="updateCalendar"
        ref='calendar'
        >
        <template slot="eventDetailsLocation" slot-scope="{ details }">
          <!-- Location -->
            <v-select
            single-line solo flat
            prepend-icon="location_on"
            :items="$locations"
            :readonly="details.locked"
            v-model="details.location">
            <template slot="item" slot-scope="{ item }">
              <v-list-tile-content>
                {{ item }}
              </v-list-tile-content>
            </template>
          </v-select>
        </template>

        <!-- Description -->
        <template slot="eventDetailsDescription" slot-scope="{ details }">
          <v-textarea v-if="$dayspan.supports.description"
            hide-details single-line solo flat
            prepend-icon="subject"
            label="Add Description"
            :readonly="details.locked"
            v-model="details.description"
          ></v-textarea>
        </template>

        <template slot="eventDetailsExtra" slot-scope="{ details }">
          <!-- Calendar -->
          <v-select
            single-line hide-details solo flat
            prepend-icon="event"
            :items="$calendarTypes"
            :readonly="details.locked"
            v-model="details.calendarType">
            <template slot="item" slot-scope="{ item }">
              <v-list-tile-content>
                {{ item }}
              </v-list-tile-content>
            </template>
          </v-select>

          <!-- Professor -->
          <v-text-field 
            single-line hide-details solo flat
            prepend-icon="school"
            label="Professor/Organiser"
            :readonly="details.locked"
            v-model="details.professor"
          ></v-text-field>

          <!-- Class -->
          <v-text-field 
            single-line hide-details solo flat
            prepend-icon="group"
            label="Participants"
            :readonly="details.locked"
            v-model="details.classEnrolled"
          ></v-text-field>

          <!-- Suggestion by -->
          <v-text-field 
            v-if="details.suggestedBy"
            single-line hide-details solo flat
            prepend-icon="feedback"
            label="Suggested By"
            disabled
            v-model="details.suggestedBy"
          ></v-text-field>

          <!-- Status -->
          <v-text-field 
            single-line hide-details solo flat
            :prepend-icon="details.locked ? 'lock' : 'lock_open'"
            :label="details.locked ? 'First Draft' : 'Suggestible'"
            disabled
            v-model="details.requestedBy"
          ></v-text-field>
        </template>
      </ds-weekly-calendar>
    </div>
  </div>
</template>

<script>
import { Calendar } from 'dayspan';
import dsWeeklyCalendarSuggestable from '../components/DaySpanWeeklyCalendarSuggestable.vue';
import dsWeeklyCalendar from '../components/DaySpanWeeklyCalendar.vue';

export default {
  name: 'WeeklyCalendarSuggestable',
  props: {
    events: {
      type: Object
    },
  },
  components: {
    dsWeeklyCalendarSuggestable,
    dsWeeklyCalendar
  },
  data: vm => ({
    calendar: Calendar.weeks(),
    isSuggesting: false
  }),
  computed: {
    suggestibleEvents(){
      return this.events.locked.concat(this.events.suggestible);
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
