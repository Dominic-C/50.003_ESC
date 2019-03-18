<template>
  <div class="courses">
    <div class="holder">
      <!-- <select v-model="selected">
        <option disabled value="">Please select one</option>
        <option v-for="(course, index) in courseList" :key="index">{{ course.courseName }}</option>
      </select> -->
      <form @submit.prevent="addCourse">
        <input list="courseSearchList" id="courseSearched" name="courseSearched" placeholder="Search for a course" v-model="courseSearched">
        <datalist id="courseSearchList">
          <option v-for="(course, index) in notEnrolledClasses" :key="index" v-bind:disabled="course.isEnrolled">{{ course.courseName }}</option>
        </datalist>
      </form>
      <ul>
        <li v-for="(data, index) in coursesEnrolled" :key='index'>{{ data.courseName }}</li>
      </ul>

      <p>These are the courses you are currently enrolled in</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Courses',
  data() {
    return {
      courseSearched: "",
      courseList: [
        {"courseName": "50.003 Elements of Software Constructions",
          "id": "50.003",
          "isEnrolled": true},
        {"courseName": "50.005 Computer Systems Engineering",
        "id": "50.005",
        "isEnrolled": true},
        {"courseName": "50.034 Probability and Statistics",
        "id": "50.034",
        "isEnrolled": true},
        {"courseName": "50.004 Algorithms",
        "id": "50.004",
        "isEnrolled": false},
        {"courseName": "01.112 Machine Learning",
        "id": "01.112",
        "isEnrolled": false},
        {"courseName": "50.040 Natural Language Processing",
        "id": "50.040",
        "isEnrolled": false},
        {"courseName": "50.006 User Interface",
        "id": "50.006",
        "isEnrolled": false}
      ], 
      coursesEnrolled: [
        {"courseName": "50.003 Elements of Software Constructions",
          "id": "50.003",
          "isEnrolled": true},
        {"courseName": "50.005 Computer Systems Engineering",
        "id": "50.005",
        "isEnrolled": true},
        {"courseName": "50.034 Probability and Statistics",
        "id": "50.034",
        "isEnrolled": true}
      ]
    }
  },
  methods: {
    addCourse() {
      // for (course in this.courseList){
      //   if (this.courseList.id === this.courseSearched){
      //   this.coursesEnrolled.push(course)
      // }   
      for (var course of this.courseList) {
        if (this.courseSearched == course.courseName){
          course.isEnrolled = true;
          this.coursesEnrolled.push({courseName: this.courseSearched});

        }
      }
      this.courseSearched = '';
    }
  },
  computed: {
    notEnrolledClasses() {
      return this.courseList.filter((course => !(course in this.coursesEnrolled)))
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
    padding: 20px;
    font-size: 1.3em;
    background-color: #E0EDF4;
    border-left: 5px solid #3EB3F6;
    margin-bottom: 2px;
    color: #3E5252;
  }

  p {
    text-align:center;
    padding: 30px 0;
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