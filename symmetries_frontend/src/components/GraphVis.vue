<template>
  <v-lazy
    v-if="vis !== ''"
  >
    <iframe
      width="100%" height="320px" :srcdoc="htmlDecode(vis)"
    />
  </v-lazy>
  <v-progress-circular
    v-else
    :size="150"
    indeterminate
    color="blue"
  />
</template>

<script>
import axios from 'axios'
import { htmlDecode } from '@/functions/functions'
import URL_BASE from '@/constants'

export default {
  name: 'GraphVis',
  methods: { htmlDecode },
  props: ['graph'],
  data () {
    return {
      vis: ''
    }
  },
  mounted () {
    axios.get(URL_BASE + 'api/vis/', {
      params: {
        data: JSON.stringify(this.graph)
      }
    }).then(res => {
      this.vis = res.data.vis
    })
  }
}
</script>

<style scoped>

</style>
