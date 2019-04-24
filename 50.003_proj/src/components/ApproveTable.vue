<template>
  <v-container>
    <v-data-table
		:headers="headers"
    :headers-length="7"
		:items="suggestions"
    :item-key="suggesting ? 'suggestedBy' : 'requestedBy'"
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
          <td class="text-xs-center">{{ suggesting ? props.item.suggestedBy : props.item.requestedBy }}</td>
          <td class="text-xs-center">{{ props.item.submittedOn }}</td>
          <td :class="[props.item.locationConflict ? 'red' : '']"></td>
          <td :class="[props.item.classConflict ? 'red' : '']"></td>
          <td :class="[props.item.professorConflict ? 'red' : '']"></td>
          <td class="text-xs-center">{{ props.item.status }}</td>
          <td :class="[props.item.status!=='Pending' ? 'grey' : '', 'justify-center align-center layout px-0']">
            <v-tooltip bottom v-if="props.item.status === 'Pending'">
              <template v-slot:activator="{ on }">
                <v-icon color="green" v-on="on" @click.stop="showApproveDialog(props.item)">check</v-icon>
              </template>
              <span>Accept {{ suggesting? 'Suggestion' : 'Request'}}</span>
            </v-tooltip>
            
            <v-tooltip bottom v-if="props.item.status === 'Pending'">
              <template v-slot:activator="{ on }">
                <v-icon color="red" v-on="on" @click.stop="showRejectDialog(props.item)">close</v-icon>
              </template>
              <span>Reject {{ suggesting? 'Suggestion' : 'Request'}}</span>
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
            <!-- Suggested by -->
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
          @click="showDialog"
        >
          Push Edit
        </v-btn>
      </template>

      <!-- Edited & Suggested by -->
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

      <!-- confirm dialog -->
      <template slot="title">
        <v-card-title class="headline">Modify suggestions?</v-card-title>
      </template>
      <template slot="text">
        <v-card-text>
          Push the modifications you have made to database for you to send to the timetable planner eventually. 
          Modifications cannot be reverted or re-edited again.
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

    <!-- Confirm Accept -->
    <app-calendar-confirm-dialog :dialog="approveDialog">
      <template slot="title">
        <v-card-title class="headline">Accept {{ suggesting ? "suggestion" : "request"}}?</v-card-title>
      </template>
      <template slot="text">
        <v-card-text>
          Approve of the  {{ suggesting ? "suggested" : "requested" }} change.
          Approval cannot be rescinded once given.
        </v-card-text>
      </template>
      <template slot="noButton">
      <v-btn
          color="green darken-1"
          flat="flat"
          @click="approveDialog = false"
        >
          Cancel
        </v-btn>
      </template>
      <template slot="yesButton">
        <v-btn
          color="green darken-1"
          flat="flat"
          @click="approve()"
        >
          OK
        </v-btn>
      </template>
		</app-calendar-confirm-dialog>

    <!-- Reject Dialog -->
    <app-calendar-confirm-dialog :dialog="rejectDialog">
      <template slot="title">
        <v-card-title class="headline">Reject {{ suggesting ? "suggestion" : "request"}}?</v-card-title>
      </template>
      <template slot="text">
        <v-card-text>
          Reject the  {{ suggesting ? "suggested" : "requested" }} change. This cannot be undone.
        </v-card-text>
      </template>
      <template slot="noButton">
      <v-btn
          color="green darken-1"
          flat="flat"
          @click="rejectDialog = false"
        >
          Cancel
        </v-btn>
      </template>
      <template slot="yesButton">
        <v-btn
          color="green darken-1"
          flat="flat"
          @click="reject()"
        >
          OK
        </v-btn>
      </template>
		</app-calendar-confirm-dialog>
  </v-container>
</template>

<script>
import * as moment from 'moment';
import { Calendar, Day } from 'dayspan';
import AppCalendar from "../components/AppCalendar";
import AppCalendarConfirmDialog from "../components/AppCalendarConfirmDialog"

export default {
  name: 'ApproveTable',
  components: {
    AppCalendar,
    AppCalendarConfirmDialog
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
      type: Boolean,
      required: true      
    },
    suggestions: {
      type: Array,
      required: true
    }
  },
	data: () => ({
    dayCalendar: Calendar.days(),
    eventsToShow: [],
    dialog: false,
    approveDialog: false,
    rejectDialog: false,
    isEditing: false,
    itemChosen: {},
    activeComp: {
      table : true,
      calendar : false,
    },
    mockData:[
      {
        suggestedBy: 'Prof A',
        status: "Pending",
        submittedOn: moment('01 Mar 2019 09:30').format('MMMM D YYYY (dddd) h:mm:ss a'),
        locationConflict: true,
        classConflict: false,
        professorConflict: false,
        conflict: [
          {
            "data": {
              "courseName": "50.003 Elements of Software Constructions",
              "pillar": "ISTD",
              "id": "001",
              "title": "50.003 Tutorial",
              "color": "#9C27B0",
              "location": "2.501",
              "professor": "Sun Jun",
              "classEnrolled": "F01",
              "calendarType": "Academic",
              "locked": null,
              "suggestedBy": null,
              "isSelected": false
            },
            "schedule": {
              "dayOfWeek": [1],
              "times": ["09:00"],
              "duration": 60,
              "durationUnit": "minutes"
            }
          },
          {
            "data": {
              "courseName": "50.003 Elements of Software Constructions",
              "pillar": "ISTD",
              "id": "002",
              "title": "50.003 Tutorial",
              "color": "#1976d2",
              "location": "2.501",
              "professor": "Sudipta",
              "classEnrolled": "F02",
              "calendarType": "Academic",
              "locked": null,
              "suggestedBy": "Prof A",
              "isSelected": false
            },
            "schedule": {
              "dayOfWeek": [1],
              "times": ["09:30"],
              "duration": 60,
              "durationUnit": "minutes"
            }
          }
        ]
      },
      {
        suggestedBy: 'Prof B',
        "requestedBy": null,
        status: "Pending",
        submittedOn: moment('24 Mar 2019 11:34:00').format('MMMM D YYYY (dddd) h:mm:ss a'),
        locationConflict: false,
        classConflict: true,
        professorConflict: false,
        conflict: [
          {
            "data": {
              "courseName": "50.003 Elements of Software Constructions",
              "pillar": "ISTD",
              "id": "001",
              "title": "50.003 Tutorial",
              "color": "#9C27B0",
              "location": "2.501",
              "professor": "Sun Jun",
              "classEnrolled": "F01",
              "calendarType": "Academic",
              "locked": null,
              "suggestedBy": null,
              "requestedBy": null,
              "isSelected": false
            },
            "schedule": {
              "dayOfWeek": [2],
              "times": ["10:00"],
              "duration": 60,
              "durationUnit": "minutes"
            }
          },
          {
            "data": {
              "courseName": "50.003 Elements of Software Constructions",
              "pillar": "ISTD",
              "id": "002",
              "title": "50.005 Tutorial",
              "color": "#1976d2",
              "location": "2.507",
              "professor": "Gemma Roig",
              "classEnrolled": "F01",
              "calendarType": "Academic",
              "locked": null,
              "suggestedBy": "Prof B",
              "requestedBy": null,
              "isSelected": false
            },
            "schedule": {
              "dayOfWeek": [2],
              "times": ["10:30"],
              "duration": 60,
              "durationUnit": "minutes"
            }
          }
        ]
      }
    ]
  }),
  computed: {
    headers(){
      let headers = [
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
      if (this.suggesting){
        headers.unshift({ text: 'Suggested By', value: 'suggestedBy' });
      }
      else {
        headers.unshift({ text: 'Requested By', value: 'requestedBy' });
      }
      return headers;
    }
  },
  methods: {
    approve(){
      //TO CHANGE: update database
      this.itemChosen.status = "Accepted";
      this.approveDialog = false;
    },
    reject(item){
      //TO CHANGE: update database
      this.itemChosen.status = "Rejected";
      this.rejectDialog = false;
    },
    showDialog(item){
      this.itemChosen = item;
      this.dialog = true;
    },
    showApproveDialog(item){
      this.itemChosen = item;
      this.approveDialog = true;
    },
    showRejectDialog(item){
      this.itemChosen = item;
      this.rejectDialog = true;
    },
    async showCalendar(props){
      props.expanded = !props.expanded;
      if (props.expanded){
        await this.$nextTick(); //waiting for calendar to be rendered
        this.$refs.expandedCalendar.$refs.calendar.viewDay(new Day(this.$termStartDate.clone().day(props.item.conflict[0].schedule.dayOfWeek)));
      }
    },
    async goToCalendar(item){
      this.toggleVisible('calendar');
      this.$emit("view-conflicts", item); 
      await this.$nextTick(); //waiting for possible conflicting events to be calculated
      this.eventsToShow = this.possibleConflictingEvents.concat(item.conflict);
      this.$refs.editCalendar.$refs.calendar.viewDay(new Day(this.$termStartDate.clone().day(item.conflict[0].schedule.dayOfWeek)));
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



