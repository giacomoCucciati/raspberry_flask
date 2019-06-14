<template>
<nav class="navbar is-link" role="navigation" aria-label="main navigation">
  <router-link to="/init-page" class="navbar-item" active-class="is-active">Initialization</router-link>
  <router-link to="/webgui-main" class="navbar-item" active-class="is-active">Web GUI</router-link>
  <router-link to="/webcam" class="navbar-item" active-class="is-active">Webcam</router-link>
  <router-link to="/dqm" class="navbar-item" active-class="is-active">DQM</router-link>
</nav>
</template>

<script>
export default {
  name: 'navbar'
}
</script>

<style>
</style>
