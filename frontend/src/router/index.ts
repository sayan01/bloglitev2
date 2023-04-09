import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import localstorage from '@/localstorage'
import { apiClient, setAuthToken } from '@/axios'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', name: 'login', component: () => import('../views/LoginView.vue') },
    { path: '/', name: 'home', component: HomeView, meta: { requiresAuth: true } },
    { path: '/logout', name: 'logout', component: () => import('../views/LogoutView.vue'), meta: { requiresAuth: true } },
  ]
})

router.beforeEach(async (to) =>{
  if(!to.meta.requiresAuth) return true
  const token = localstorage.get('token')
  if(!token) return { name: 'login' }
  // check if token is valid
  setAuthToken(token)
  const resp = (await apiClient.get('/user/login')).status
  if(resp !== 200) return { name: 'login' }
  return true
})


export default router
