<template>
  <v-container>
    <structure-component
      url="http://127.0.0.1:8000/api/petersen/"
      :params="{}"
      :refresh="counter"
    />
  </v-container>
</template>

<script>
import StructureComponent from '@/components/Structure'

export default {
  name: 'PetersenComponent',
  components: { StructureComponent },
  data () {
    return {
      counter: 0
    }
  },
  mounted () {
    this.counter++
  }
}
</script>

<style scoped>

</style>
