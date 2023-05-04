<template>
  <v-lazy>
    <v-table
      density="compact"
    >
      <tbody>
      <tr
          v-for="row in dClass"
          :key="row"
      >
        <td
            v-for="cell in row"
            :key="cell"
        >
          <v-icon
            v-if="cell.is_group"
            icon="mdi-information"
            style="position: relative; float: right"
            @click="findGroupInfo(cell.data)"
          />
          <TableSpan :cell-data="cell.data" />
        </td>
      </tr>
      </tbody>
      <v-dialog
        v-model="dialog"
        width="auto"
      >
        <v-card
          class="mx-2 px-4"
          max-width="400"
        >
          <v-card-title>
            Group information
            <v-icon
              icon="mdi-close"
              @click="dialog = false"
              class="ml-3"
              style="position: relative; float: right"
            />
          </v-card-title>
          <table-span :cell-data="selectedGroup" /> <br>
          <div v-if="!this.loading">
            <span style="font-weight: bold">Group:</span> {{ groupType }} <br>
            <span style="font-weight: bold">Group description:</span> {{ groupDesc }} <br>
            <span style="font-weight: bold">Order:</span> {{ selectedGroup.length }} <br>
            <span style="font-weight: bold">Identity:</span> {{ identity }} <br>
          </div>
          <v-progress-circular
            v-else
            :size="60"
            color="blue"
            indeterminate
            class="ma-3"
          />
        </v-card>
      </v-dialog>
    </v-table>
  </v-lazy>
</template>

<script>
import axios from 'axios'
import TableSpan from '@/components/TableSpan'
import URL_BASE from '@/constants'

export default {
  name: 'TableComponent',
  components: { TableSpan },
  props: ['dClass'],
  data () {
    return {
      rowLength: 0,
      dialog: false,
      selectedGroup: undefined,
      groupType: undefined,
      identity: undefined,
      groupDesc: undefined,
      loading: true
    }
  },
  methods: {
    findGroupInfo (data) {
      this.loading = true
      this.groupDesc = undefined
      this.identity = undefined
      this.groupType = undefined
      this.dialog = true
      this.selectedGroup = data
      const payload = JSON.stringify(data)
      axios.get(URL_BASE + 'api/groupinfo/', {
        params: {
          data: payload
        }
      }).then(res => {
        this.groupType = res.data.groupType
        this.identity = res.data.identity
        this.groupDesc = res.data.groupDesc
        this.loading = false
      }).catch(err => {
        console.log(err)
      })
    }
  }
}
</script>

<style scoped>
table, td, tr {
  border: 2px solid black;
}
</style>
