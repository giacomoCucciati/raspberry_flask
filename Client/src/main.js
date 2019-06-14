// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Buefy from 'buefy'
// import 'buefy/lib/buefy.css'
import App from './App'
import router from './router'
import VueAxios from 'vue-axios'
import axios from 'axios'
import Highcharts from 'highcharts'
import VueHighcharts from 'highcharts-vue'

Vue.use(VueAxios, axios)
Vue.use(Buefy)
Vue.use(VueHighcharts, {Highcharts})
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
