<template>
  <div
    class="font-weight-bold text-h4 text-red"
  >
    {{ errorMsg }}
  </div>
  <main-sym-navigation :sizes="sizes" />
  <v-row
    v-for="(res, i) in responses"
    :key="res"
    :set="res.show = false"
    :index="i"
    style="margin-bottom: 3%;"
    ref="scrollContainer"
  >
    <v-col>
      <div
        style="text-align: center; font-weight: bold; font-size: large"
        :id="res.vertices + 'V' + res.edges + 'E'"
      >
        Vertices: {{ res.vertices}}, Edges: {{ res.edges }}
      </div>
      <graph-vis
        v-if="i !== responses.length - 1"
        :graph="res.graph"
      />
      <table-component
        v-if="res.size < 100 || res.show"
        :d-class="res.result"
      />
      <v-btn
        v-else
        @click="res.show = true"
        color="blue"
      >
       Show table
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
import axios from 'axios'
import { htmlDecode } from '@/functions/functions'
import TableComponent from '@/components/Table'
import MainSymNavigation from '@/components/MainSymNavigation'
import GraphVis from '@/components/GraphVis'
import URL_BASE from '@/constants'

export default {
  name: 'StructureComponent',
  components: { GraphVis, MainSymNavigation, TableComponent },
  props: ['url', 'params', 'refresh'],
  data () {
    return {
      responses: [],
      sizes: new Map(),
      lastProcessedChunk: 0,
      errorMsg: ''
    }
  },
  watch: {
    refresh () {
      this.getAsymmetricGraphPartialSymmetries()
    }
  },
  methods: {
    htmlDecode,
    getAsymmetricGraphPartialSymmetries () {
      this.responses = []
      this.sizes.clear()
      this.errorMsg = ''
      this.lastProcessedChunk = -1
      axios.get(URL_BASE + this.url, {
        params: this.params,
        onDownloadProgress: (event) => {
          let nextChunkStart = 0
          let nextChunkEnd = 0
          while (nextChunkEnd !== -1) {
            const string = event.event.currentTarget.responseText
            nextChunkStart = string.indexOf('{"chunk": ' + (this.lastProcessedChunk + 1).toString())
            nextChunkEnd = string.indexOf('{"chunk": ' + (this.lastProcessedChunk + 2).toString())
            const input = nextChunkEnd !== -1 ? string.substring(nextChunkStart, nextChunkEnd) : string.substring(nextChunkStart)
            const parsedInput = JSON.parse(input)
            if (parsedInput.error === 'timeout') {
              this.errorMsg = 'Execution timed out!'
            }
            this.responses.push(parsedInput)
            this.lastProcessedChunk += 1
            for (const item of this.responses) {
              if (!this.sizes.has(item.vertices)) {
                this.sizes.set(item.vertices, new Set([item.edges]))
              } else {
                this.sizes.get(item.vertices).add(item.edges)
              }
            }
          }
        } }
      )
    }
  }
}
</script>

<style scoped>

</style>
