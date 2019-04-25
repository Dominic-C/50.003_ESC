<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :headers-length="4"
		  :items="suggestions"
      item-key="submittedOn"
		  class="elevation-1"
      v-if="activeComp.table"
    >
      <template v-slot:headers="props">
        <th class="text-xs-center" v-for="prop in props.headers" :key="prop.text">{{ prop.text }}</th>
      </template>

      <!-- table rows -->
      <template v-slot:items="props">
        <tr @click="showCalendar(props)">
          <td class="text-xs-center">{{ props.item.bookedBy }}</td>
          <td class="text-xs-center">{{ props.item.submittedOn }}</td>
          <td class="text-xs-center">{{ props.item.status }}</td>
          <td class="justify-center align-center layout px-0">            
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon v-on="on" @click.stop="showRemoveDialog(props.item)" v-if="props.item.status==='Booked'">delete</v-icon>
              </template>
              <span>Remove Booking</span>
            </v-tooltip>
            
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon v-on="on" @click.stop="goToCalendar(props.item)">visibility</v-icon>
              </template>
              <span>View/edit in Calendar</span>
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
          </app-calendar>
        </v-flex>
      </template>
    </v-data-table>

    <app-calendar 
      v-if="activeComp.calendar" 
      :calendar="dayCalendar"
      :username="username"
      :isInMode="isEditing"
      :dialog="dialog"
      mode="editable"
      ref="editCalendar"
    >
      <template slot="switchModeButton">
        <v-layout justify-space-between> 
          <v-btn 
            color="grey"
            @click="toggleVisible('table')"
          >
            <v-icon dark left>arrow_back</v-icon>Back
          </v-btn>
          <v-btn 
            color="primary"
            @click="isEditing = !isEditing"
          >
            Edit
          </v-btn>
        </v-layout>
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
          @click="showRemoveDialog"
        >
          Push Edit
        </v-btn>
      </template>

      <!-- Edited & Booked by -->
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

    <!-- Remove Dialog -->
    <app-calendar-confirm-dialog :dialog="removeDialog">
      <template slot="title">
        <v-card-title class="headline">Remove booking?</v-card-title>
      </template>
      <template slot="text">
        <v-card-text>
          Remove the  bookings made. This is immediately applied to the finalised table and cannot be undone, but the event can be booked again.
        </v-card-text>
      </template>
      <template slot="noButton">
      <v-btn
          color="green darken-1"
          flat="flat"
          @click="removeDialog = false"
        >
          Cancel
        </v-btn>
      </template>
      <template slot="yesButton">
        <v-btn
          color="green darken-1"
          flat="flat"
          @click="remove"
        >
          OK
        </v-btn>
      </template>
    </app-calendar-confirm-dialog>
  </v-container>
</template>

<script>
import { Calendar, Day, Units } from 'dayspan';
import AppCalendar from "../components/AppCalendar";
import AppCalendarConfirmDialog from "../components/AppCalendarConfirmDialog"

export default {
  name: 'BookingsTable',
  components: {
    AppCalendar,
    AppCalendarConfirmDialog
  },
  props: {
    username: {
      type: String,
      required: true
    },
    suggestions: {
      type: Array,
      required: true
    }
  },
	data: () => ({
    dayCalendar: Calendar.days(),
    dialog: false,
    approveDialog: false,
    removeDialog: false,
    isEditing: false,
    itemChosen: {},
    activeComp: {
      table : true,
      calendar : false,
    },
    headers: [{ text: 'Booked By', value: 'bookedBy' },
        { text: 'Submitted On', value: 'submittedOn' },
        { text: 'Status', value: 'status' },
        { text: 'Actions', value: 'action', sortable: false }]
  }),
  methods: {
    remove(){
      //TO CHANGE: update database
      this.itemChosen.status = "Removed";
      this.removeDialog = false;
    },
    showDialog(item){
      this.itemChosen = item;
      this.dialog = true;
    },
    showRemoveDialog(item){
      this.itemChosen = item;
      this.removeDialog = true;
    },
    async showCalendar(props){
      props.expanded = !props.expanded;
      if (props.expanded){
        await this.$nextTick(); //waiting for calendar to be rendered
        let state = Calendar.fromInput(JSON.parse(props.item.calendar));
        state.preferToday = false;
        this.$refs.expandedCalendar.$refs.calendar.setState(state);
      }
    },
    async goToCalendar(item){
      this.toggleVisible('calendar');
      await this.$nextTick(); //waiting for possible conflicting events to be calculated
      let state = Calendar.fromInput(JSON.parse(item.calendar));
    state.preferToday = false;
    this.$refs.editCalendar.$refs.calendar.setState(state);
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
    },
    pushToDatabase(){
      this.dialog = false;
      this.isEditing = false;
      //TO CHANGE: update database and check for conflicts
      this.itemChosen.status = "Edited";
    }
  }
}
</script>



