import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home'
import Custom from '../views/Custom'

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
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
