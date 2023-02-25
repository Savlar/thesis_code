<template>
  <main-sym-navigation :sizes="sizes" />
  <v-row
    v-for="(res, i) in responses"
    :key="res"
    :index="i"
    style="margin-bottom: 3%;"
  >
    <v-col>
      <div
        style="text-align: center; font-weight: bold; font-size: large"
        :id="res.vertices + 'V' + res.edges + 'E'"
      >
        Vertices: {{ res.vertices}}, Edges: {{ res.edges }}
      </div>
      <iframe
          v-if="i !== responses.length - 1"
          width="100%" height="320px" :srcdoc="htmlDecode(res.vis)"/>
      <table-component
        :d-class="res.result"
      />
    </v-col>
  </v-row>
</template>

<script>
import axios from 'axios'
import { htmlDecode } from '@/functions/functions'
import TableComponent from '@/components/Table.vue'
import MainSymNavigation from '@/components/MainSymNavigation.vue'

export default {
  name: 'StructureComponent',
  components: { MainSymNavigation, TableComponent },
  props: ['url', 'params', 'refresh'],
  data () {
    return {
      responses: [],
      sizes: new Map(),
      lastProcessedChunk: 0
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
      this.lastProcessedChunk = 0
      axios.get(this.url, {
        params: this.params,
        onDownloadProgress: (event) => {
          let nextChunkStart = 0
          let nextChunkEnd = 0
          while (nextChunkEnd !== -1) {
            const string = event.event.currentTarget.responseText
            nextChunkStart = string.indexOf('{"chunk": ' + (this.lastProcessedChunk + 1).toString())
            nextChunkEnd = string.indexOf('{"chunk": ' + (this.lastProcessedChunk + 2).toString())
            const input = nextChunkEnd !== -1 ? string.substring(nextChunkStart, nextChunkEnd) : string.substring(nextChunkStart)
            this.responses.unshift(JSON.parse(input))
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
