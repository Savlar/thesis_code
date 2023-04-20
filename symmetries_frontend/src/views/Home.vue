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
    <structure :url="'http://127.0.0.1:8000/api/asymgraph/' + this.selectedAsymmetricGraph + '/'" :params="{}" :refresh="counter" />
  </v-container>
</template>

<script>
import { htmlDecode } from '@/functions/functions'
import Structure from '@/components/Structure.vue'
import axios from 'axios'

export default {
  name: 'HomeView',
  data () {
    return {
      asymmetricGraphs: ['X1,X8', 'X2,X7', 'X3,X6', 'X4,X5', 'X9,X14', 'X10,X13', 'X11,X12', 'X15,X18', 'X16,X17'],
      selectedAsymmetricGraph: 'X1,X8',
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
      console.log('here')
      axios.get('http://127.0.0.1:8000/api/asym_vis/', {
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
