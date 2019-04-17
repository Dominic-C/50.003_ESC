<template>
  <div>
		<v-layout justify-end pb-3>	
    	<template v-if="!isInMode">
				<slot name="switchModeButton">
					<v-btn color="primary">Modify</v-btn>
				</slot>
			</template>
			<template v-else>
				<slot name="cancelButton">
					<v-btn color="grey">Cancel</v-btn>
				</slot>
				<slot name="pushButton">
					<v-btn color="primary">Push</v-btn>
				</slot>
			</template>
		</v-layout>
    <div style="height: 500px">
			<ds-weekly-calendar 
				:events="events" 
				:calendar="calendar" 
				:suggestible="isSuggestible" 
				:requestable="isRequestable"
				:read-only="!isInMode"
				:username="username"
				@event-update="updateCalendar"
				ref='calendar'
				>
				<template slot="eventDetailsLocation" slot-scope="{ details }">
					<!-- Location -->
						<v-select
						single-line solo flat
						prepend-icon="location_on"
						label="Add Location"
						:items="$locations"
						:readonly="!isInMode || details.locked"
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
						:readonly="!isInMode || details.locked"
						v-model="details.description"
					></v-textarea>
				</template>

				<template slot="eventDetailsExtra" slot-scope="{ details }">
					<!-- Calendar -->
					<v-select
						single-line hide-details solo flat
						prepend-icon="event"
						:items="$calendarTypes"
						:readonly="!isInMode || details.locked"
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
						:readonly="!isInMode || details.locked"
						v-model="details.professor"
					></v-text-field>

					<!-- Class -->
					<v-text-field 
						single-line hide-details solo flat
						prepend-icon="group"
						label="Participants"
						:readonly="!isInMode || details.locked"
						v-model="details.classEnrolled"
					></v-text-field>

					<!-- Suggestion by -->
					<v-text-field 
						v-if="mode==='suggestible'&& details.suggestedBy"
						single-line hide-details solo flat
						prepend-icon="feedback"
						label="Suggested By"
						disabled
						v-model="details.suggestedBy"
					></v-text-field>
					
					<!-- Requested by -->
					<v-text-field 
						v-if="mode==='requestable' && details.requestedBy"
						single-line hide-details solo flat
						prepend-icon=""
						label="Requested By"
						disabled
						v-model="details.requestedBy"
					></v-text-field>

					<!-- Status -->
					<template v-if="mode==='suggestible'">
						<v-text-field 
							single-line hide-details solo flat
							:prepend-icon="details.locked ? 'lock' : 'lock_open'"
							:label="details.locked ? 'First Draft' : 'Suggested Change'"
							disabled
							v-model="details.suggestBy"
						></v-text-field>
					</template>
					<template v-else-if="mode==='requestable'">
						<v-text-field 
							single-line hide-details solo flat
							:prepend-icon="details.locked ? 'lock' : 'lock_open'"
							:label="details.locked ? 'Current Calendar' : 'Requested Change'"
							disabled
							v-model="details.requestedBy"
						></v-text-field>
					</template>
				</template>
			</ds-weekly-calendar>
    </div>
  </div>
</template>

<script>
import { Calendar } from 'dayspan';
import dsWeeklyCalendar from '../components/DaySpanCalendar.vue';

export default {
  name: 'ModifiableCalendar',
  props: {
    events: {
      type: Array
    },
    username: {
      type: String,
      required: true
    },
    mode: {
      type: String,
      validator: function (value) {
        //check that it is in either suggestible or requestable mode
        return ['suggestible', 'requestable'].indexOf(value) !== -1
      }
		},
		isInMode: {
			type: Boolean
		}
  },
  components: {
    dsWeeklyCalendar
  },
  data: () => ({
		calendar: Calendar.weeks(),
  }),
  computed: {
		isSuggestible(){
			return this.mode==="suggestible";
		},
		isRequestable(){
			return this.mode==="requestable";
		}
  },
  methods: {
    updateCalendar(event){
      this.$emit('event-update', event);	//from DaySpanCalendar 
    },
    applyEvents(){
      this.$refs.calendar.applyEvents();	//from App.vue to DaySpanCalendar
		}
  }  
}
</script>
