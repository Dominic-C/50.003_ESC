<template>
  <!-- <v-form @submit.prevent> -->
    <v-container fluid class="pa-4">
      <v-layout wrap>
        <v-flex xs12>
          <v-autocomplete
            v-model="itemsSelected"
            :items="searchTable[searchCategory]"
            item-value="searchText"
            chips
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
                @input="remove(data.item.searchText)"
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
              <v-list-tile-content @click="updateCalendar(data.item.searchText)">
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
  <!-- </v-form> -->
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
      itemsSelected: [],  
      searchCategories: [
        {text: 'Course Name', value: 'courseName', table: this.courseNameTable}, 
        {text: 'Class', value: 'classEnrolled', table: this.classTable}, 
        {text: 'Professor', value: 'professor', table: this.professorTable}, 
        {text: 'Location', value: 'location', table: this.locationTable}
      ],
      searchTable: {
        courseName: this.courseNameTable, 
        classEnrolled: this.classTable, 
        professor: this.professorTable, 
        location: this.locationTable
      },
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
      // var selectionCandidates = this.searchableItems.filter((searchObject, index) => {
      //   const indexOfIndenticalObject = searchList.findIndex(item => item[this.searchCategory] === searchObject[this.searchCategory]);
      //   return indexOfIndenticalObject === index;
      // });  
      return this.searchTable[this.searchCategory];
    }
  },
  watch: {
    itemsSelected: function (newList, oldList) {
      if (newList.length === 0){
        for (var item of oldList){
          this.remove(item);
        }
      }
    },
    searchCategory: function (newCategory, oldCategory){
      if (oldCategory != ''){
        for (var item of this.searchTable[oldCategory]){
          this.$emit('selected-search-item', {item: item.searchText, searchCategory: oldCategory, isSelected: false});
        }
        this.itemsSelected = [];
      }
    }
  },
  methods: {
    remove (item) {
      const index = this.itemsSelected.indexOf(item)
      if (index >= 0) {
        this.itemsSelected.splice(index, 1);  //deleting item from itemsSelected array
      }
      this.$emit('selected-search-item', {item: item, searchCategory: this.searchCategory, isSelected: false});
    },
    updateCalendar(item) {
      this.$emit('selected-search-item', {item: item, searchCategory: this.searchCategory, isSelected: !this.itemsSelected.includes(item)});
    }  
  }
}
</script>