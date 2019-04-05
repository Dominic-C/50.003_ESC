<template>
  <v-form @submit.prevent>
    <v-container fluid class="pa-4">
      <v-layout wrap>
        <v-flex xs12>
          <v-autocomplete
            v-model="coursesSelected"
            :items="courseList"
            chips
            return-object
            item-text="courseName"
            label="Search for courses to add"
            multiple
            clearable
            no-data-text="No such available course name"
          >
            <!-- item that appears in search bar -->
            <template v-slot:selection="data">
              <v-chip
                :selected= "data.selected"
                close
                class="chip--select-multi"
                @input="remove(data.item)"
              >
                <v-icon 
                  :color="getColour(data.item)"
                  class="headline font-weight-heavy white--text" 
                  left>
                    {{ data.item.pillar.substring(0, 2) }}
                  </v-icon>
                <span v-text="data.item.courseName"></span>
              </v-chip>
            </template>
            <!-- list of items that appear on search -->
            <template v-slot:item="data">
              <v-list-tile-avatar
                v-bind:color="getColour(data.item)"
                class="headline font-weight-light white--text"
              >
                {{ data.item.pillar.substring(0, 2) }}
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title v-text="data.item.courseName"></v-list-tile-title>
                <v-list-tile-sub-title v-html="data.item.pillar"></v-list-tile-sub-title>
              </v-list-tile-content>
            </template>
          </v-autocomplete>

          <!-- choosing search category -->
          <v-select
            single-line solo flat
            label="Search Category"
            :items="searchCategories"
            v-model="searchCategory">
            <template slot="item" slot-scope="{ item }">
              <v-list-tile-content>
                {{ item }}
              </v-list-tile-content>
            </template>
          </v-select>
        </v-flex>
      </v-layout>
    </v-container>
  </v-form>
</template>

<script>
export default {
  name: 'SearchCourses',
  data: () => ({
    searchCategories: ['Course Name', 'Class', 'Professor', 'Location']
  }),
  methods: {
    remove (item) {
      item.isSelected = false;
    },
    getColour(item) {
      if (item.pillar === "ISTD") {
        return "indigo";
      } 
      else if (item.pillar == "ESD") {
        return "red";
      }
      else if (item.pillar == "EPD") {
        return "blue";
      }
      else if (item.pillar == "ASD") {
        return "purple";
      }
      else if (item.pillar == "FRESHMORE") {
        return "green";
      }
      else if (item.pillar == "HASS") {
        return "pink";
      }
    }
  },
  computed: {
    coursesSelected: {
      get: function() {
        return this.courseList.filter(course => course.isSelected);
      },
      set: function(courses) {
        for (var course of this.courseList){
          this.remove(course);
        }
        for (var courseSelected of courses){
          courseSelected.isSelected = true;
        }
        // for (var course of courses){
        //   console.log(course);
        // }
      }
    }
  },
  props: {
    courseList: {
      type: Array,
      required: true
    }
  }
}
</script>