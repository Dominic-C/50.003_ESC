<template>
  <div>
		<v-layout justify-end pb-3>	
    	<template v-if="!isInMode">
				<slot name="switchModeButton"/>
			</template>
			<template v-else>
				<slot name="cancelButton"/>
				<slot name="pushButton"/>
			</template>
		</v-layout>
    <div style="height: 500px">
			<ds-calendar 
				:events="events" 
				:calendar="calendar" 
				:suggestible="isSuggestible" 
				:requestable="isRequestable"
				:editable="isEditable"
				:read-only="!isInMode"
				:username="username"
				@event-update="updateCalendar"
				ref='calendar'
				>
				<template slot="eventDetailsLocation" slot-scope="{ details }">
					<!-- Location -->
					<template v-if="mode==='finalised' || (mode==='requestable' && details.locked === true)">
						<v-text-field 
							single-line hide-details solo flat
							prepend-icon="location_on"
							label="Add Location"
							:items="$locations"
							:readonly="!isInMode || details.locked"
							v-model="details.location">
						</v-text-field>
					</template>
					<template v-else>
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
						label="Event Type"
						:readonly="!isInMode || details.locked"
						v-model="details.calendarType">
						<template slot="item" slot-scope="{ item }">
							<v-list-tile-content>
								{{ item }}
							</v-list-tile-content>
						</template>
					</v-select>

					<v-select
						v-if="details.calendarType === 'Academic'"
						single-line  solo flat
						prepend-icon="view_column"
						:items="$pillars"
						label="Pillar"
						:readonly="!isInMode || details.locked"
						v-model="details.pillar">
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

					<!-- Additional comments -->
					<v-textarea v-if="isInMode && (isSuggestible || isRequestable)"
						hide-details single-line solo flat
						prepend-icon="comment"
						label="Add Comments"
						:readonly="!isInMode || details.locked"
						v-model="details.comments"
					></v-textarea>

					<!-- Status -->
					<slot name="status" v-bind="{ details }"></slot>

					<!-- Suggested/Edited/Requested by -->
					<slot name="additionalInfo" v-bind="{ details }"></slot>

				</template>

				<template slot="eventPopover" slot-scope="slotData">
					<ds-calendar-event-popover
						v-bind="slotData"
						:read-only="!isInMode"
					></ds-calendar-event-popover>
				</template>

				<template slot="eventTimeTitle" slot-scope="{calendarEvent, details}">
					<div>
						<v-icon class="ds-ev-icon"
							v-if="details.icon"
							size="14"
							:style="{color: details.forecolor}">
							{{ details.icon }}
						</v-icon>
						<strong class="ds-ev-title">{{ details.title }}</strong>
					</div>
					<div class="ds-ev-description">{{ getCalendarTime( calendarEvent ) }}</div>
				</template>
			</ds-calendar>
    </div>

		<div>
			<app-calendar-confirm-dialog :dialog="dialog">
				<template slot="title"><slot name="title"></slot></template>
				<template slot="text"><slot name="text"></slot></template>
				<template slot="noButton"><slot name="noButton"></slot></template>
				<template slot="yesButton"><slot name="yesButton"></slot></template>
			</app-calendar-confirm-dialog>
		</div>
  </div>
</template>

<script>
import { Calendar } from 'dayspan';
import dsCalendar from '../components/DaySpanCalendar.vue';
import AppCalendarConfirmDialog from "../components/AppCalendarConfirmDialog";

export default {
  name: 'AppCalendar',
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
        return ['suggestible', 'requestable', 'editable', 'finalised'].indexOf(value) !== -1
      }
		},
		isInMode: {
			type: Boolean,
			default(){
				return false;
			} 
		},
		calendar: {
			type: Calendar
		},
		dialog: {
			type: Boolean,

		}
  },
  components: {
		dsCalendar,
		AppCalendarConfirmDialog
  },
  data: () => ({
  }),
  computed: {
		isSuggestible(){
			return this.mode==="suggestible";
		},
		isRequestable(){
			return this.mode==="requestable";
		},
		isEditable(){
			return this.mode==="editable";
		}
  },
  methods: {
    updateCalendar(event){
      this.$eventHub.$emit('event-update', event);
    },
		getCalendarTime(calendarEvent){
      let sa = calendarEvent.start.format('a');
      let ea = calendarEvent.end.format('a');
      let sh = calendarEvent.start.format('h');
      let eh = calendarEvent.end.format('h');
      if (calendarEvent.start.minute !== 0)
      {
        sh += calendarEvent.start.format(':mm');
      }
      if (calendarEvent.end.minute !== 0)
      {
        eh += calendarEvent.end.format(':mm');
      }
      return (sa === ea) ? (sh + ' - ' + eh + ea) : (sh + sa + ' - ' + eh + ea);
    }
  }  
}
</script>
