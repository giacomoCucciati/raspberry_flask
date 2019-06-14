<template>
  <div id="app">
    <navbar/>
    <router-view/>
  </div>
</template>

<script>
import navbar from './components/navbar.vue'

export default {
  name: 'App',
  components: { navbar }
}
</script>

<style>

</style>

<style lang="scss">
// Import Bulma's core
// @import 'bulma';
@import "~bulma/sass/utilities/_all";

// $box-radius: 0;
// $section-padding: 1.5rem 1rem;
$navbar-background-color: $blue;
$navbar-item-color : $white;

// Import Bulma and Buefy styles
@import "bulma";
</style>
