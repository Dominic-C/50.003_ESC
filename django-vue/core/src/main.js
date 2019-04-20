// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import App from "./App.vue";
import Vuetify from "vuetify";
import DaySpanVuetify from "dayspan-vuetify";

import "./plugins/vuetify";
import * as moment from "moment";

import "vuetify/dist/vuetify.min.css";
import "material-design-icons-iconfont/dist/material-design-icons.css";
import "dayspan-vuetify/dist/lib/dayspan-vuetify.min.css";

Vue.config.productionTip = false;

Vue.use(Vuetify);

Vue.use(DaySpanVuetify, {
  data: {
    supports: {
      color: false,
      busy: false,
      icon: false,
      calendar: false
    }
  },
  methods: {
    getDefaultEventColor: () => "#1976d2"
  }
});

Vue.prototype.$calendarTypes = ["Academic", "Events"];
Vue.prototype.$locations = [
  "Unspecified",
  "Lecture Theatre 1",
  "Lecture Theatre 2",
  "Lecture Theatre 3",
  "Lecture Theatre 4",
  "Lecture Theatre 5"
];
Vue.prototype.$termStartDate = moment([2019, 8, 16]);
Vue.prototype.$eventHub = new Vue(); // Global event bus
/* eslint-disable no-new */

new Vue({
  el: "#app",
  components: { App },
  template: "<App/>"
});
