<template>
  <v-btn
    icon="mdi-chevron-up"
    size="large"
    class="homebtn"
    color="blue"
    @click="scrollToTop"
  />
</template>

<script>
export default {
  name: 'TopScroll',
  methods: {
    scrollToTop () {
      window.scrollTo(0, 0)
    }
  }
}
</script>

<style scoped>
  .homebtn {
    position: fixed;
    right: 1%;
    bottom: 7%;
    z-index: 999;
  }
</style>
