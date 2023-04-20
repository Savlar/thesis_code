<template>
  <v-container>
    <v-select
      v-model="selected"
      :items="types"
      @update:model-value="counter++"
    />
  </v-container>
  <petersen-component v-if="selected === 'Petersen Graph'" />
  <complete-component v-if="selected === 'Complete Graph'" />
</template>

<script>
import PetersenComponent from '@/components/Petersen'
import CompleteComponent from '@/components/Complete'

export default {
  name: 'TypesView',
  components: { CompleteComponent, PetersenComponent },
  data () {
    return {
      types: ['Petersen Graph', 'Complete Graph'],
      counter: 0,
      selected: undefined
    }
  },
  methods: {
  }
}
</script>

<style scoped>

</style>
