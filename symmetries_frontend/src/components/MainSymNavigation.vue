<template>
  <v-container>
    <v-row
      v-for="vertexCount in Array.from(this.sizes.keys()).reverse()"
      :key="vertexCount"
    >
      <v-col
        style="font-weight: bold"
      >
        <div>
          {{ vertexCount }} <span v-if="vertexCount !== 1">vertices:</span><span v-else>vertex:</span>
        </div>
      </v-col>
      <v-col
        v-for="edgeCount in Array.from(this.sizes.get(vertexCount)).sort()"
        :key="edgeCount"
        style="align-content: center"
      >
        <v-btn
          @click="scrollToTable(vertexCount + 'V' + edgeCount + 'E')"
          color="blue"
        >
          {{ edgeCount }} edge <span v-if="edgeCount !== 1">s</span>
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'MainSymNavigation',
  props: ['sizes'],
  methods: {
    scrollToTable (tableId) {
      const el = document.getElementById(tableId)
      el.scrollIntoView()
    }
  }
}
</script>

<style scoped>

</style>
