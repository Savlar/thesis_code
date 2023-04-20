import { defineStore } from 'pinia'
import axios from 'axios'

export const customGraphStore = defineStore('custom', {
  state: () => ({
    graphData: [[], []],
    interval: undefined,
    customGraphVis: undefined,
    vertexCount: 2,
    lastChanged: undefined,
    lastValue: undefined,
    counter: 0
  }),
  getters: {
  },
  actions: {
    vertexCountChanged () {
      while (this.graphData.length < this.vertexCount) {
        this.graphData.push([])
      }
      while (this.graphData.length > this.vertexCount) {
        this.graphData.pop()
      }
      for (let i = 0; i < this.graphData.length; i++) {
        this.graphData[i] = this.graphData[i].filter(i => i <= this.vertexCount)
      }
      this.getGraphVis()
    },
    update (index) {
      clearInterval(this.interval)
      const neighbours = this.graphData[index]
      for (const neighbour of neighbours) {
        if (this.graphData[neighbour - 1].indexOf(index + 1) === -1) {
          this.graphData[neighbour - 1].push(index + 1)
        }
      }
      for (let i = 0; i < this.graphData.length; i++) {
        if (i !== index && this.graphData[i].indexOf(index + 1) !== -1 && neighbours.indexOf(i + 1) === -1) {
          this.graphData[i].splice(this.graphData[i].indexOf(index + 1), 1)
        }
      }
      if (this.lastChanged !== index) {
        this.lastValue = this.counter
      }
      this.counter++
      this.lastChanged = index
      this.interval = setInterval(this.getGraphVis, 500)
    },
    remove (index, value) {
      this.graphData[index].splice(this.graphData[index].indexOf(value), 1)
      this.graphData[value - 1].splice(this.graphData[value - 1].indexOf(index + 1), 1)
      this.counter++
      this.lastChanged = this.vertexCount + 1
      this.interval = setInterval(this.getGraphVis, 500)
    },
    getGraphVis () {
      const payload = JSON.stringify(this.graphData)
      axios.get('http://127.0.0.1:8000/api/graphvis/', {
        params: {
          data: payload,
          vertexCount: this.vertexCount
        }
      }).then(res => {
        this.customGraphVis = res.data.vis
        clearInterval(this.interval)
      }).catch(err => {
        console.log(err)
      })
    }
  }
})
