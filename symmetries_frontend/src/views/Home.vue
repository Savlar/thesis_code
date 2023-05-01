<template>
  <v-container>
    <v-row>
      <v-col>
        <v-select
          v-model="selectedAsymmetricGraph"
          :items="asymmetricGraphs"
          @update:model-value="getGraphVis"
          solo
        />
      </v-col>
    </v-row>
    <v-row>
      <iframe width="100%" height="320px" :srcdoc="htmlDecode(vis)"/>
    </v-row>
  </v-container>
  <v-container>
    <structure :url="'/api/asymgraph/' + this.selectedAsymmetricGraph + '/'" :params="{}" :refresh="counter" />
  </v-container>
</template>

<script>
import { htmlDecode } from '@/functions/functions'
import Structure from '@/components/Structure.vue'
import axios from 'axios'
import URL_BASE from '@/constants'

export default {
  name: 'HomeView',
  data () {
    return {
      asymmetricGraphs: ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10', 'X11', 'X12', 'X13', 'X14', 'X15', 'X16', 'X17', 'X18'],
      selectedAsymmetricGraph: 'X1',
      counter: 0,
      vis: ''
    }
  },
  components: {
    Structure
  },
  methods: {
    htmlDecode,
    getGraphVis () {
      this.counter++
      axios.get(URL_BASE + 'api/asym_vis/', {
        params: {
          data: this.selectedAsymmetricGraph
        }
      }).then(res => {
        this.vis = res.data.vis
      })
    }
  },
  mounted () {
    this.getGraphVis()
  }
}
</script>

<style scoped>

</style>
