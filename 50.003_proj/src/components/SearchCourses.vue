<template>
  <!-- <div class="courses"> -->
    <div>
      <!-- <select v-model="selected">
        <option disabled value="">Please select one</option>
        <option v-for="(course, index) in courseList" :key="index">{{ course.courseName }}</option>
      </select> -->
      <v-app id="inspire">
        <v-form @submit.prevent>
          <v-container fluid>
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
                        v-bind:color="getColour(data.item)"
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
                      <v-list-tile-title        v-text="data.item.courseName"></v-list-tile-title>
                      <v-list-tile-sub-title v-html="data.item.pillar"></v-list-tile-sub-title>
                    </v-list-tile-content>
                  </template>
                </v-autocomplete>
              </v-flex>
            </v-layout>
          </v-container>
        </v-form>
      </v-app>
      <!-- previous search method -->
      <!-- <form @submit.prevent="addCourse">
        <input list="courseSearchList" id="coursesSelected" name="coursesSelected" placeholder="Search for a course" v-model="coursesSelected">
        <datalist id="courseSearchList">
          <option v-for="(course, index) in notEnrolledClasses" :key="index" v-bind:disabled="course.isSelected">{{ course.courseName }}</option>
        </datalist>
      </form> -->
      
    <!-- </div> -->
  </div>
</template>

<script>
export default {
  name: 'SearchCourses',
  data() {
    return {
      courseList: [
        {"courseName": "50.003 Elements of Software Constructions",
          "id": "50.003",
          "pillar": "ISTD",
          "isSelected": true},
        {"courseName": "50.005 Computer Systems Engineering",
        "id": "50.005",
        "pillar": "ESD",
        "isSelected": true},
        {"courseName": "50.034 Probability and Statistics",
        "id": "50.034",
        "pillar": "EPD",
        "isSelected": true},
        {"courseName": "50.004 Algorithms",
        "id": "50.004",
        "pillar": "ASD",
        "isSelected": false},
        {"courseName": "01.112 Machine Learning",
        "id": "01.112",
        "pillar": "FRESHMORE",
        "isSelected": false},
        {"courseName": "50.040 Natural Language Processing",
        "id": "50.040",
        "pillar": "HASS",
        "isSelected": false},
        {"courseName": "50.006 User Interface",
        "id": "50.006",
        "pillar": "ISTD",
        "isSelected": false}
      ]
      // coursesEnrolled: [
      //   {"courseName": "50.003 Elements of Software Constructions",
      //     "id": "50.003",
      //     "pillar": "ISTD",
      //     "isSelected": true},
      //   {"courseName": "50.005 Computer Systems Engineering",
      //   "id": "50.005",
      //   "pillar": "ISTD",
      //   "isSelected": true},
      //   {"courseName": "50.034 Probability and Statistics",
      //   "id": "50.034",
      //   "pillar": "ISTD",
      //   "isSelected": true}
      // ]
    }
  },
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
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .holder {
    background: #fff;
  }
  ul {
    margin: 0;
    padding: 0;
    list-style-type: none;
  }
  
  ul li {
    padding: 10px;
    font-size: 1em;
    background-color: #E0EDF4;
    border-left: 5px solid #3EB3F6;
    margin-bottom: 2px;
    color: #3E5252;
  }
  p {
    text-align:center;
    padding: 5px 0;
    color: gray;
  }
  .container {
    box-shadow: 0px 0px 40px lightgray;
  }
  input {
    width: calc(100% - 40px);
    border: 0;
    padding: 20px;
    font-size: 1.3em;
    background-color: #323333;
    color: #687F7F;
  }
  .alert {
    background: #fdf2ce;
    font-weight: bold;
    display: inline-block;
    padding: 5px;
    margin-top: -20px;
  }
</style>