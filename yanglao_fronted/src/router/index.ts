import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  // {
  //   path: '/',
  //   name: 'detect',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import( '../views/OrderDetection.vue')
  // },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    children: [
        {
            path: '/OrderDetection',
            name: 'OrderDetection',
            component: () => import('../views/OrderDetection.vue'),
            // children: [
            //     {
            //         path: 'user',
            //         name: 'user',
            //         component: () => import('../views/User.vue'),
            //     },
            //     {
            //         path: 'menu',
            //         name: 'menu',
            //         component: () => import('../views/Menu.vue'),
            //     },
            // ]
        },
        {
          path: '/DetectionBatch',
          name: 'DetectionBatch',
          component: () => import('../views/DetectionBatch.vue'),
      },
    ]
},
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
