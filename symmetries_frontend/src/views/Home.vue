<template>
  <v-container>
    <v-row>
      <v-col>
        <v-select
          v-model="selectedAsymmetricGraph"
          :items="asymmetricGraphs"
          @update:model-value="counter++"
          solo
        />
      </v-col>
    </v-row>
<!--    <v-row v-if="original !== null">-->
<!--      <iframe width="100%" height="320px" :srcdoc="htmlDecode(original)"/>-->
<!--    </v-row>-->
  </v-container>
  <v-container>
    <structure :url="'http://127.0.0.1:8000/api/asymgraph/' + this.selectedAsymmetricGraph + '/'" :params="{}" :refresh="counter" />
  </v-container>
</template>

<script>
import { htmlDecode } from '@/functions/functions'
import Structure from '@/components/Structure.vue'

export default {
  name: 'HomeView',
  data () {
    return {
      asymmetricGraphs: ['X1,X8', 'X2,X7', 'X3,X6', 'X4,X5', 'X9,X14', 'X10,X13', 'X11,X12', 'X15,X18', 'X16,X17'],
      selectedAsymmetricGraph: 'X1,X8',
      counter: 0
    }
  },
  components: {
    Structure
  },
  methods: {
    htmlDecode
  },
  mounted () {
    this.counter++
  }
}
</script>

<style scoped>

</style>
