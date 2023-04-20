import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home'
import Custom from '../views/Custom'
import Types from '../views/Types.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/custom',
    name: 'Custom',
    component: Custom
  },
  {
    path: '/types',
    name: 'Types',
    component: Types
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
