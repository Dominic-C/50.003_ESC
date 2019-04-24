<template>
    <v-app id="dayspan" v-cloak>
      <app-header @changeComp="toggleVisible"></app-header>
      <v-content>
        <search-bar></search-bar>
        <finalised-calendar></finalised-calendar>
      </v-content>
    </v-app>
</template>

<script>
import AppHeader from "../components/AppHeader.vue"
import SearchBar from '../components/SearchBarVue'
import FinalisedCalendar from '../components/FinalisedCalendar.vue';

export default {
  components: {
      AppHeader,
      SearchBar, 
      FinalisedCalendar
  },
  methods: {
    update(item){
      this.$emit('changeComp', item);
    }
  }
}
</script>
