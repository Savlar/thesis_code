<template>
  <div
    class="font-weight-bold text-h4 text-red"
  >
    {{ errorMsg }}
  </div>
  <v-container
    v-if="value > 0 && value < 95"
  >
    <v-row justify="center">
      <v-progress-circular
        :model-value="value"
        size="100"
        width="20"
        color="blue"
      >
        {{ value }}
      </v-progress-circular>
    </v-row>
  </v-container>
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
  props: ['url', 'params', 'refresh', 'vertices', 'reset'],
  data () {
    return {
      responses: [],
      sizes: new Map(),
      lastProcessedChunk: 0,
      errorMsg: '',
      loading: false,
      value: 0
    }
  },
  watch: {
    refresh () {
      this.getAsymmetricGraphPartialSymmetries()
    },
    reset () {
      this.responses = []
      this.value = 0
      this.sizes.clear()
      this.errorMsg = ''
    }
  },
  methods: {
    htmlDecode,
    getAsymmetricGraphPartialSymmetries () {
      this.responses = []
      this.value = 0
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
            this.value += 100 / this.vertices
          }
        }
      }
      )
    }
  }
}
</script>

<style scoped>

</style>
