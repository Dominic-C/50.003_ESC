import Vue from "vue";
import "./plugins/vuetify";
import Vuetify from "vuetify";
import App from "./App.vue";
import DaySpanVuetify from "dayspan-vuetify";
import * as moment from 'moment';

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
      },
      defaults: {
        dsCalendarEventPopover: {
          allowEditOnReadOnly: false
        },
        dsEventDialog: {
          dialogProps: {
            persistent: false,
            lazy: true,
            maxWidth: '800px'
          }
        }
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

new Vue({
  render: h => h(App)
}).$mount("#app");
