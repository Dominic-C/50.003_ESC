<template>
  <v-container>
    <!-- <b-button @click="toggleBusy">Toggle Busy State</b-button>
    <b-table responsive 
      :busy="isBusy" 
      :items="items"
      selectable
      :select-mode="single"
      selectedVariant="success">
      <div slot="table-busy" class="text-center text-danger my-2">
        <b-spinner class="align-middle"></b-spinner>
        <strong>Loading...</strong>
      </div>
    </b-table> -->

    <!-- <div class="table-responsive  table-hover">
      <table class="table">
        <th colspan="3"></th>
        <td class="bg-primary">...</td>
        <td class="bg-success">...</td>
        <td class="bg-warning">...</td>
        <td class="bg-danger">...</td>
        <td class="bg-info">...</td>
      </table>
    </div>
   -->
		<v-data-table
		:headers="headers"
    :headers-length="6"
		:items="suggestions"
    item-key="suggestedBy"
		class="elevation-1"
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
        <td class="justify-center align-center layout px-0">
          <v-icon
          color="green"
            @click="approve(props.item)"
          >
            check
          </v-icon>
          <v-icon
          color="red"
            @click="reject(props.item)"
          >
            close
          </v-icon>
          </td>
      </tr>
		</template>

    <!-- Calendar view -->
    <template v-slot:expand="props">
      <v-flex class="pa-4" style="height:500px">
        <finalised-calendar 
          :events="props.item.conflict" 
          :calendar="dayCalendar"
        ></finalised-calendar>
      </v-flex>
      </template>
	</v-data-table>
  </v-container>
</template>

<script>
import { Calendar, Day } from 'dayspan';
import FinalisedCalendar from "../components/FinalisedCalendar";

export default {
  name: 'ViewResultsTable',
  components: {
    FinalisedCalendar
  },
	data: () => ({
    dayCalendar: Calendar.days(),
		headers: [
			{ text: 'Suggested By', value: 'suggestedBy' },
			{ text: 'Submitted On', value: 'submittedOn' },
      { text: 'Conflicts', value: 'conflicts', children: 
        [
          {text: 'Location', value: 'location'},
          {text: 'Class', value: 'class'},
          {text: 'Professor', value: 'professor'}
        ]
      },
      { text: 'Actions', value: 'name', sortable: false }

    ],
    suggestions:[
      {
        suggestedBy: 'Prof A',
        submittedOn: new Date('01 Mar 2019 09:30:00'),
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
              "requestedBy": null,
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
              "suggestedBy": null,
              "requestedBy": null,
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
        submittedOn: new Date('24 Mar 2019 11:34:00'),
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
              "title": "50.005 Tutorial",
              "color": "#1976d2",
              "location": "2.507",
              "professor": "Gemma Roig",
              "classEnrolled": "F01",
              "calendarType": "Academic",
              "locked": null,
              "suggestedBy": null,
              "requestedBy": null,
              "isSelected": false
            },
            "schedule": {
              "dayOfWeek": [2],
              "times": ["09:30"],
              "duration": 60,
              "durationUnit": "minutes"
            }
          }
        ]
      }
    ]
  }),
  methods: {
    approve(){
      console.log("approved")
    },
    reject(){
      console.log("rejected")
    },
    showCalendar(props){
      props.expanded = !props.expanded;
      this.$eventHub.$emit('view-day', new Day(this.$termStartDate.day(props.item.conflict[0].schedule.dayOfWeek)));
    }
  }
}
</script>



