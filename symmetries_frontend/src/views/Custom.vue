<template>
  <v-container>
    <v-row>
      <v-col
        cols="2"
      >
        Number of vertices: {{ customStore.vertexCount }}
      </v-col>
      <v-col>
        <v-slider
          v-model="customStore.vertexCount"
          :min="2"
          :max="10"
          :step="1"
          @update:model-value="changedGraph"
        />
      </v-col>
    </v-row>
    <v-container
      v-for="key in [...Array(customStore.vertexCount).keys()]"
      :key="key"
    >
      Enter neighbours of element {{ key + 1 }}
      <neighbour-selector
        :id="key"
        :choices="[...Array(customStore.vertexCount).keys()].filter(i => i !== key).map(i => i + 1)"
        @reset="reset++"
      />
    </v-container>
    <v-row>
      <iframe
        v-if="customStore.customGraphVis !== undefined"
        width="100%" height="320px" :srcdoc="htmlDecode(customStore.customGraphVis)"
      />
    </v-row>
    <v-row
      justify="center"
    >
      <v-btn
        @click="counter++"
        class="mt-3"
        color="blue"
      >
        Get partial automorphisms
      </v-btn>
    </v-row>
  </v-container>
  <v-container>
    <structure-component
      url="api/customsym/"
      :params="{
        data: JSON.stringify(this.customStore.graphData)
      }"
      :refresh="counter"
      :vertices="customStore.vertexCount"
      :reset="reset"
    />
  </v-container>
</template>

<script>
import NeighbourSelector from '@/components/NeighbourSelector'
import { htmlDecode } from '@/functions/functions'
import { mapStores } from 'pinia'
import { customGraphStore } from '@/stores/customGraph'
import StructureComponent from '@/components/Structure'

export default {
  name: 'CustomView',
  components: { StructureComponent, NeighbourSelector },
  data () {
    return {
      responses: [],
      sizes: new Map(),
      lastProcessedChunk: 0,
      counter: 0,
      reset: 0
    }
  },
  computed: {
    // access as customStore
    ...mapStores(customGraphStore)
  },
  methods: {
    htmlDecode,
    changedGraph () {
      this.reset++
      this.customStore.vertexCountChanged()
    }
  },
  mounted () {
    this.customStore.getGraphVis()
  }
}
</script>

<style scoped>

</style>
