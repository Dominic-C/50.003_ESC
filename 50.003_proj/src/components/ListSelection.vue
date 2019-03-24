<template>
    <v-container fluid>
        <v-layout wrap>
            <v-flex xs12>
                <p>These are the courses you have selected:</p>
                <ul>
                    <li v-for="course in coursesSelected" :key="course.id">
                    {{ course.courseName }}</li>
                </ul>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
export default {
  name: 'SearchCourses',
  props: {
    courseList: {
      type: Array,
      required: true
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
  methods: {
    remove (item) {
      item.isSelected = false;
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