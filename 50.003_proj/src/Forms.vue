<template>
  <div>
    <v-app id="inspire">
      <app-header></app-header>
      <form-submit :formFields="formFields"></form-submit>
    </v-app>
  </div>
</template>

<script>
import AppHeader from './components/AppHeader.vue';
import FormSubmit from './components/FormSubmit.vue';
export default {
  name: 'forms',
  data: () => ({
    courseList: [
      ]
  }),
  components: {
    AppHeader,
    FormSubmit
  }
}
</script>  