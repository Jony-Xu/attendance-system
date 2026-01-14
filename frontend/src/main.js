import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import 'semantic-ui-css/semantic.min.css'
import App from './App.vue'
import EmployeeAttendance from './components/EmployeeAttendance.vue'
import AdminDashboard from './components/AdminDashboard.vue'

const routes = [
  { path: '/', redirect: '/employee' },
  { path: '/employee', component: EmployeeAttendance },
  { path: '/admin', component: AdminDashboard }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
