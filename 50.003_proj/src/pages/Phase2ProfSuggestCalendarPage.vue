<template>
  <v-app id="dayspan" v-cloak>
    <app-header @changeComp="toggleVisible"></app-header>
    <v-content>
      <search-bar></search-bar>
      <suggestible-calendar></suggestible-calendar>
    </v-content>
  </v-app>
</template>

<script>
import AppHeader from "../components/AppHeader.vue";
import SearchBar from '../components/SearchBar.Vue'
import SuggestibleCalendar from '../components/SuggestibleCalendar.vue';

export default {
  components: {
    AppHeader,
    SearchBar, 
    SuggestibleCalendar
  },
  methods: {
    update(item){
      this.$emit('changeComp', item);
    }
  }
}
</script>
