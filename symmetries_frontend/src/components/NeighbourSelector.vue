<template>
  <div>
    <v-select
      v-model="customStore.graphData[id]"
      :key="refresh"
      :id="'customSelect' + id"
      :items="choices"
      multiple
      @update:model-value="update(id)"
    />
    <v-row>
      <div
        v-for="neighbour in customStore.graphData[id]"
        :key="neighbour"
      >
        <v-avatar
          class="ma-1"
          color="blue"
        >
          {{ neighbour }}
        </v-avatar>
        <v-btn
          variant="text"
          size="small"
          icon="mdi-close"
          style="position: relative; top: -40%; right: 25%"
          @click="remove(id, neighbour)"
        >
        </v-btn>
      </div>
    </v-row>
  </div>
</template>

<script>
import { customGraphStore } from '@/stores/customGraph'
import { mapStores } from 'pinia'

export default {
  name: 'NeighbourSelector',
  props: ['id', 'choices'],
  computed: {
    // access as customStore
    ...mapStores(customGraphStore),
    refresh () {
      if (this.id !== this.customStore.lastChanged) {
        return this.customStore.counter
      }
      return this.customStore.lastValue
    }
  },
  methods: {
    update (id) {
      this.$emit('reset')
      this.customStore.update(id)
    },
    remove (id, neighbour) {
      this.$emit('reset')
      this.customStore.remove(id, neighbour)
    }
  }
}
</script>

<style scoped>

</style>
