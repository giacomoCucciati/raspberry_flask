<template>
  <div>
    <div>
      <b-field label="Port list">
        <b-select placeholder="Select a port" v-model='selectedPort'>
          <option
            v-for="port in port_list"
            :value="port"
            :key="port">
            {{ port }}
          </option>
        </b-select>
      </b-field>
      <button v-on:click="startReadXbee">Start reading xbee</button>
      <button v-on:click="stopReadXbee">Stop reading xbee</button>
      <button v-on:click="fakeAcquisition">Fake points</button>
      <div v-if="this.chartOptions !== undefined">
        <highcharts :options="chartOptions" ref="lineCharts"></highcharts>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import io from 'socket.io-client'

export default {
  name: 'InitPage',
  data () {
    return {
      port_list: [],
      light_points: [],
      temperature_points: [],
      selectedPort: '',
      chartOptions: {
        series: []
      }
    }
  },

  methods: {
    startReadXbee: function () {
      console.log('Selected port: ', this.selectedPort)
      axios.post('/api/startXbee', {selectedPort: this.selectedPort}).then(response => {
        console.log(response)
      })
    },

    stopReadXbee: function () {
      axios.get('/api/stopXbee').then(response => {
        console.log(response)
      })
    },

    fakeAcquisition: function () {
      axios.get('/api/startFakeAcq').then(response => {
        console.log(response)
      })
    },

    updatePage: function () {
      axios.get('/api/getPageUpdate').then(response => {
        this.port_list = response.data.portlist
        this.selectedPort = response.data.selectedPort

        response.data.pointList.forEach(point => {
          this.light_points.push([point.timestamp, point.light])
          this.temperature_points.push([point.timestamp, point.temperature])
        })
      })
    },

    defineChartOptions () {
      this.chartOptions['chart'] = {
        type: 'scatter',
        zoomType: 'x'
      }
      this.chartOptions['title'] = {
        text: 'Calibration Sequence'
        // margin: -44
      }
      this.chartOptions['xAxis'] = {
        title: {
          text: 'Time'
        },
        type: 'datetime',
        dateTimeLabelFormats: {
          second: '%H:%M:%S'
        }
      }
      this.chartOptions['yAxis'] = {
        title: {
          text: 'FED nb'
        },
        min: 0,
        max: 1024
      }
      this.chartOptions['plotOptions'] = {
        series: {
          animation: false
        }
      }
      this.chartOptions['series'].push({
        name: 'Temperature',
        color: 'rgba(3, 169, 244, 0.7)',
        data: this.temperature_points,
        marker: {
          symbol: 'cyrcle'
        }
      })
      this.chartOptions['series'].push({
        name: 'Light',
        color: 'rgba(0, 255, 0, 0.7)',
        data: this.light_points,
        marker: {
          symbol: 'cyrcle'
        }
      })
    },

    askOnePoint () {
      // console.log('Request from server to get the last point.')
      axios.get('/api/getSinglePoint').then(r => {
        // console.log(r)
        this.light_points.push([r.data.singlePoint.timestamp, r.data.singlePoint.light])
        this.temperature_points.push([r.data.singlePoint.timestamp, r.data.singlePoint.temperature])
        if (this.light_points.length > 1000) {
          this.light_points.shift()
        }
        if (this.temperature_points.length > 1000) {
          this.temperature_points.shift()
        }
        // console.log(this.temperature_points)
        // console.log(this.light_points)
      })
    }
  },

  mounted () {
    // Asking all of the parameters to draw the page
    this.updatePage()

    // Creating the socket for updates notifications
    this.socket = io()

    // Callback for update event
    this.socket.on('updateSinglePoint', () => this.askOnePoint())

    this.defineChartOptions()
  },

  beforeRouteLeave (to, from, next) {
    this.socket.close()
    next()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
