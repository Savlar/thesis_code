<template>
  <span
      v-for="(value, index) in cellData"
      :key="value"
      :style="[index % 2 === 0 ? {'text-align': 'left'} : {'text-align': 'right'}]"
      style="display: block"
  >
    {{ value }}<br>
  </span>
</template>

<script>
export default {
  name: 'TableSpan',
  props: ['cellData']
}
</script>

<style scoped>

</style>
