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
      <b-field label="Port list 2">
        <b-select placeholder="Select a port" v-model='selectedPort2'>
          <option
            v-for="port in port_list"
            :value="port"
            :key="port">
            {{ port }}
          </option>
        </b-select>
      </b-field>
      <button v-on:click="startReadXbee2">Start reading xbee2</button>
      <button v-on:click="stopReadXbee2">Stop reading xbee2</button>
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
      pitemperature_points: [],
      temperatureDTH_points: [],
      humidityDTH_points: [],
      selectedPort: '',
      selectedPortExt: '',
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

    startReadXbeeExt: function () {
      console.log('Selected port: ', this.selectedPortExt)
      axios.post('/api/startXbeeExt', {selectedPort: this.selectedPortExt}).then(response => {
        console.log(response)
      })
    },

    stopReadXbeeExt: function () {
      axios.get('/api/stopXbeeExt').then(response => {
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
        this.selectedPort2 = response.data.selectedPort2

        response.data.pointList.forEach(point => {
          this.light_points.push([point.timestamp, point.lum])
          this.pitemperature_points.push([point.timestamp, point.pitemp])
          this.temperatureDTH_points.push([point.timestamp, point.tempDTH])
          this.humidityDTH_points.push([point.timestamp, point.humDTH])
        })
      })
    },

    defineChartOptions () {
      this.chartOptions['chart'] = {
        type: 'scatter',
        zoomType: 'x'
      }
      this.chartOptions['title'] = {
        text: 'Measurements'
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
          text: 'Celsius or ADC counts'
        }
        // min: 0,
        // max: 1024
      }
      this.chartOptions['plotOptions'] = {
        series: {
          animation: false
        }
      }
      this.chartOptions['series'].push({
        name: 'PI Temp',
        color: 'rgba(233, 233, 0, 0.7)',
        data: this.pitemperature_points,
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
      this.chartOptions['series'].push({
        name: 'TempDTH',
        color: 'rgba(255, 0, 0, 0.7)',
        data: this.temperatureDTH_points,
        marker: {
          symbol: 'cyrcle'
        }
      })
      this.chartOptions['series'].push({
        name: 'HumDTH',
        color: 'rgba(125, 125, 125, 0.7)',
        data: this.humidityDTH_points,
        marker: {
          symbol: 'cyrcle'
        }
      })
    },

    askOnePoint () {
      // console.log('Request from server to get the last point.')
      axios.get('/api/getSinglePoint').then(r => {
        // console.log(r)
        this.light_points.push([r.data.singlePoint.timestamp, r.data.singlePoint.lum])
        this.pitemperature_points.push([r.data.singlePoint.timestamp, r.data.singlePoint.pitemp])
        this.temperatureDTH_points.push([r.data.singlePoint.timestamp, r.data.singlePoint.tempDTH])
        this.humidityDTH_points.push([r.data.singlePoint.timestamp, r.data.singlePoint.humDTH])
        if (this.light_points.length > 1000) {
          this.light_points.shift()
        }
        if (this.pitemperature_points.length > 1000) {
          this.pitemperature_points.shift()
        }
        if (this.temperatureDTH_points.length > 1000) {
          this.temperatureDTH_points.shift()
        }
        if (this.humidityDTH_points.length > 1000) {
          this.humidityDTH_points.shift()
        }
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
