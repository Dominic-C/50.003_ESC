<template>
  <v-container>
    <v-data-table
			:headers="headers"
			:headers-length="6"
			:items="suggestions"
			:item-key="suggesting ? suggestedBy : requestedBy"
			class="elevation-1"
			v-if="activeComp.table"
		>
		<!-- table headers -->
      <template v-slot:headers="props">
        <tr class="text-xs-center">
          <template v-for="prop in props.headers">
            <th v-if="!prop.children" :key="prop.text" rowspan="2" style="border-bottom: solid 2px grey;">{{ prop.text }}</th>
            <th v-else :key="prop.text" colspan="3" text-xs-center>{{ prop.text }}</th>
          </template>
        </tr>
        <tr class="text-xs-center">
          <template v-for="prop in props.headers">
            <th v-for="child in prop.children" :key="child.text" width="100px">{{ child.text }}</th>
          </template>
        </tr>
      </template>

      <!-- table rows -->
      <template v-slot:items="props">
        <tr @click="showCalendar(props)">
          <td class="text-xs-right">{{ props.item.suggestedBy }}</td>
          <td class="text-xs-right">{{ props.item.submittedOn }}</td>
          <td :class="[props.item.locationConflict ? 'red' : '']"></td>
          <td :class="[props.item.classConflict ? 'red' : '']"></td>
          <td :class="[props.item.professorConflict ? 'red' : '']"></td>
          <td class="text-xs-right">{{ props.item.status }}</td>
          <td :class="[props.item.status==='Cancelled' ? 'grey' : '', 'justify-center align-center layout px-0']">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }" v-if="props.item.status==='Cancelled'">
                <v-icon v-on="on" @click.stop="dialog = true">close</v-icon>
              </template>
              <span>Cancel {{ suggesting ? 'Suggestion' : 'Request'}}</span>
            </v-tooltip>
						<v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon v-on="on" @click.stop="goToCalendar(props.item)">visibility</v-icon>
              </template>
              <span>View in Calendar</span>
            </v-tooltip>
          </td>
        </tr>
      </template>

      <!-- Calendar view -->
      <template v-slot:expand="props">
        <v-flex class="pa-4" style="height:500px">
          <app-calendar
            :events="props.item.conflict"
            :calendar="dayCalendar"
            ref="expandedCalendar"
            username="username"
            mode="finalised"   
          >
            <!-- Suggested/Requested by -->
            <template slot="additionalInfo" slot-scope="{ details }">
              <v-layout row>
                <v-flex xs2>
                  <v-subheader v-if="details.suggestedBy">Suggested by</v-subheader>
                </v-flex>
                <v-flex xs10>
                  <v-text-field 
                    v-if="details.suggestedBy"
                    single-line hide-details solo flat
                    disabled
                    v-model="details.suggestedBy"
                  ></v-text-field>
                </v-flex>
              </v-layout>

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
          </app-calendar>
        </v-flex>
      </template>
    </v-data-table>

    <app-calendar 
      transition="slide-x-reverse-transition" 
      v-if="activeComp.calendar" 
      :events="eventsToShow"
      :calendar="dayCalendar"
      :username="username"
      :isInMode="isEditing"
      :dialog="dialog"
      mode="editable"
      ref="editCalendar"
			>

      <!-- Edited & Suggested/Requested by -->
      <template slot="additionalInfo" slot-scope="{ details }">
        <v-layout row>
          <v-flex xs2>
            <v-subheader v-if="details.suggestedBy">Suggested by</v-subheader>
          </v-flex>
          <v-flex xs10>
            <v-text-field 
              v-if="details.suggestedBy"
              single-line hide-details solo flat
              disabled
              v-model="details.suggestedBy"
            ></v-text-field>
          </v-flex>
        </v-layout>

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

				<v-layout row>
					<v-flex xs2>
						<v-subheader v-if="details.editedBy">Edited by</v-subheader>
					</v-flex>
					<v-flex xs10>
						<v-text-field 
							v-if="details.editedBy"
							single-line hide-details solo flat
							disabled
							v-model="details.editedBy"
						></v-text-field>
					</v-flex>
        </v-layout>
      </template>
    </app-calendar>

    <app-calendar-confirm-dialog :dialog="dialog">
      <template slot="title">
        <v-card-title class="headline">Cancel {{ suggesting ? "suggestion" : "request"}}?</v-card-title>
      </template>
      <template slot="text"><slot name="text">
        <v-card-text>
          Cancel the {{ suggesting ? "suggestion" : "request"}} you have made to course coordintor. 
          Cancellation cannot be undoed and will be reflected on course coordinator's side. 
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
          @click="cancel"
        >
          OK
        </v-btn>
      </template>
		</app-calendar-confirm-dialog>
  </v-container>
</template>

<script>
import { Calendar, Day } from 'dayspan';
import AppCalendar from "../components/AppCalendar";

export default {
  name: 'ViewResultsTable',
  components: {
    AppCalendar
  },
  props: {
    username: {
      type: String,
      required: true
    },
    possibleConflictingEvents: {
      type: Array,
      required: true
		},
		suggesting: {
			type: Boolean
		}
  },
	data: () => ({
    dayCalendar: Calendar.days(),
    eventsToShow: [],
    dialog: false,
    isEditing: false,
    itemChosen: [],
    activeComp: {
      table : true,
      calendar : false,
    },
		headers: [
			{ text: 'Submitted On', value: 'submittedOn' },
      { text: 'Conflicts', value: 'conflicts', children: 
        [
          {text: 'Location', value: 'location'},
          {text: 'Class', value: 'class'},
          {text: 'Professor', value: 'professor'}
        ]
      },
      { text: 'Status', value: 'status' },
      { text: 'Actions', value: 'action', sortable: false }

    ]
  }),
  methods: {
    cancel(){
      //TO CHANGE: update database
      itemChosen.status = "Cancelled"
    },
    async showCalendar(props){
      props.expanded = !props.expanded;
      if (props.expanded){
        await this.$nextTick(); //waiting for calendar to be rendered
        this.$refs.expandedCalendar.$refs.calendar.viewDay(new Day(this.$termStartDate.day(props.item.conflict[0].schedule.dayOfWeek)));
      }
    },
    async goToCalendar(item){
      this.itemChosen = item;
      this.toggleVisible('calendar');
      this.$emit("view-conflicts", item); 
      await this.$nextTick(); //waiting for possible conflicting events to be calculated
      this.eventsToShow = this.possibleConflictingEvents.concat(item.conflict);
      this.$refs.editCalendar.$refs.calendar.viewDay(new Day(this.$termStartDate.day(item.conflict[0].schedule.dayOfWeek)));
    },
    toggleVisible : function(item) {
      this.activeComp.table = false;
      this.activeComp.calendar = false;
      if(item == "table"){
        this.activeComp.table = true;
      }
      if(item == "calendar"){
        this.activeComp.calendar = true;
      }
    },
    revertState(){
      this.isEditing = false;
      this.$eventHub.$emit('apply-events');
    }
  }
}
</script>



