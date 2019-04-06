<template>
  <v-form @submit.prevent>
    <v-container fluid class="pa-4">
      <v-layout wrap>
        <v-flex xs12>
          <v-autocomplete
            v-model="itemsSelected"
            :items="selectionCandidates"
            chips
            return-object
            label="Search for courses to add"
            multiple
            clearable
            no-data-text="No such name"
            :disabled="!categoryHasBeenChosen"
          >
            <!-- how selected items should be rendered -->
            <template v-slot:selection="data">
              <v-chip
                close
                class="chip--select-multi"
                @input="remove(data.item)"
              >
                <v-icon 
                  v-if="searchCategory!=='location'" 
                  :color="pillarColours[data.item.pillar]"
                  class="headline font-weight-heavy white--text" 
                  left>
                    {{ data.item.pillar.substring(0, 2) }}
                  </v-icon>
                <span v-text="data.item.searchText"></span>
              </v-chip>
            </template>

            <!-- how list of searchable items should be rendered -->
            <template v-slot:item="data">
              <v-list-tile-avatar
                v-if="searchCategory!=='location'" 
                :color="pillarColours[data.item.pillar]"
                class="headline font-weight-light white--text"
              >
                {{ data.item.pillar.substring(0, 2) }}
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title v-text="data.item.searchText"></v-list-tile-title>
                <v-list-tile-sub-title 
                  v-if="searchCategory!=='location'" 
                  v-html="data.item.pillar">
                </v-list-tile-sub-title>
              </v-list-tile-content>
            </template>
          </v-autocomplete>

          <!-- choosing search category -->
          <v-select
            single-line solo flat
            label="Search Category"
            :items="searchCategories"
            v-model="searchCategory">
          </v-select>
        </v-flex>
      </v-layout>
    </v-container>
  </v-form>
</template>

<script>
export default {
  name: 'SearchCourses',
  props: {
    calendarEventsTable: {
      type: Array,
      required: true
    },
    professorTable: {
      type: Array,
      required: true
    },
    courseNameTable: {
      type: Array,
      required: true
    },
    locationTable: {
      type: Array,
      required: true
    },
    classTable: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      searchCategory: '',  
      searchCategories: [
        {text: 'Course Name', value: 'courseName', table: this.courseNameTable}, 
        {text: 'Class', value: 'classEnrolled', table: this.classTable}, 
        {text: 'Professor', value: 'professor', table: this.professorTable}, 
        {text: 'Location', value: 'location', table: this.locationTable}
      ],
      pillarColours: {
        ISTD: 'indigo',
        ESD:'red',
        EPD:'blue',
        ASD:'purple',
        FRESHMORE:'green',
        HASS:'pink'
      }
    }
  },
  computed: {
    categoryHasBeenChosen() {
      if (this.searchCategory !== ""){
        return true;
      }
      else {
        return false;
      }
    },
    selectionCandidates() {
      //TO CHANGE: get selection categories from database (for now, hardcoding it from front-end)
      // var selectionCandidates = [];
      // var selectionCandidatesSet = new Set();
      // if (this.searchCategory === "location"){
      //   for (var searchObject of this.searchableItems){
      //     selectionCandidatesSet.add(JSON.stringify({searchText: searchObject[this.searchCategory]}));
      //   }
      //   selectionCandidatesSet.forEach(searchObject => {
      //     selectionCandidates.push(JSON.parse(searchObject)); 
      //   });
      // }
      // else {
      //   for (var searchObject of this.searchableItems){
      //     selectionCandidatesSet.add(JSON.stringify({    //JSON.stringify so that objects can be compared
      //       searchText: searchObject[this.searchCategory], 
      //       pillar: searchObject.pillar}));
      //   }
      //   selectionCandidatesSet.forEach(searchObject => {
      //     selectionCandidates.push(JSON.parse(searchObject)); //parse back to object
      //   }); 
      // }
      // var selectionCandidates = this.searchableItems.filter((searchObject, index) => {
      //   const indexOfIndenticalObject = searchList.findIndex(item => item[this.searchCategory] === searchObject[this.searchCategory]);
      //   return indexOfIndenticalObject === index;
      // });  
           
      for (var category of this.searchCategories){
        if (category.value === this.searchCategory) {
          return category.table;
        }
      }
      return [];
    },
    itemsSelected: {
      get: function() {
        //TODO: select items through database method eventually
        // var itemsSelected = [];
        // for (var item of this.selectionCandidates){
        //   if (item.isSelected){
        //     itemsSelected.push(item);
        //   }
        // }
        // return itemsSelected;
        return this.selectionCandidates.filter(item => item.isSelected);
      },
      set: function(selectedItems) {
        for (var item of selectedItems){
          //changing ___table (database) 
          //TODO: change in database eventually
          item.isSelected = true;
          //changing calendarEventsTable (database) so that calendar can be updated
          //TODO: change in database eventually
          for (var event of this.calendarEventsTable){
            if (event.data[this.searchCategory] === item.searchText){
              event.data.isSelected === true;
            }
          }
        }
      }
    }
  },
  methods: {
    remove (item) {
      //TO CHANGE: updating calendarEventsTable
      for (var event of this.calendarEventsTable){
        if (event.data[this.searchCategory] === item.searchText){
          event.data.isSelected === false;
        }
      }
      //TO CHANGE: updating __table
      item.isSelected = false;
    }
    // getColour(item) {
    //   if (item.pillar === "ISTD") {
    //     return "indigo";
    //   } 
    //   else if (item.pillar == "ESD") {
    //     return "red";
    //   }
    //   else if (item.pillar == "EPD") {
    //     return "blue";
    //   }
    //   else if (item.pillar == "ASD") {
    //     return "purple";
    //   }
    //   else if (item.pillar == "FRESHMORE") {
    //     return "green";
    //   }
    //   else if (item.pillar == "HASS") {
    //     return "pink";
    //   }
    // }
  }
}
</script>