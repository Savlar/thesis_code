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
    console.log(this.graph)
    axios.get('http://127.0.0.1:8000/api/vis/', {
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
