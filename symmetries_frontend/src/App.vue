<template>
  <v-app>
    <v-main>
      <v-toolbar title="Partial symmetries of graphs" border>
        <v-spacer />
        <v-btn
          to="/"
        >
          Home
        </v-btn>
        <v-btn
          to="/custom"
        >
          Custom
        </v-btn>
      </v-toolbar>
      <router-view />
      <top-scroll />
    </v-main>
    <v-footer
      color="dark"
      border
      class="mt-1"
      style="max-height: 6%"
    >
      <v-row>
        <v-col
          cols="12"
          class="text-center"
          style="color: white"
        >
          2023 by Matúš Gál
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>

<script>

import TopScroll from '@/components/TopScroll'

export default {
  name: 'App',
  components: { TopScroll },

  data: () => ({
    //
  })
}
</script>
