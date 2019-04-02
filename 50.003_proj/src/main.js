import Vue from 'vue'
import './plugins/vuetify'
import Vuetify from 'vuetify'
import App from './App.vue'
import DaySpanVuetify from 'dayspan-vuetify'

import 'vuetify/dist/vuetify.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import 'dayspan-vuetify/dist/lib/dayspan-vuetify.min.css'

Vue.config.productionTip = false

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
    getDefaultEventColor: () => '#1976d2'
  }
});

Vue.prototype.$calendarTypes = ['Academic', 'Fifth Row', 'Events'];

new Vue({
  render: h => h(App),
}).$mount('#app')
