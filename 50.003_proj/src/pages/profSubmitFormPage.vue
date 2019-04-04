<template>
    <v-app>
      <app-header @changeComp="toggleVisible"></app-header>
      <v-content>
        <form-submit></form-submit>
      </v-content>
    </v-app>
</template>

<script>
import AppHeader from '../components/AppHeader.vue';
import FormSubmit from '../components/FormSubmit.vue';

export default {
    components: {
        AppHeader,
        FormSubmit
    }
    
}
</script>
