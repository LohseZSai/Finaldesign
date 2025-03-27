import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

// 公共页面
const Home = () => import('../views/public/Home.vue')
const About = () => import('../views/public/About.vue')
const News = () => import('../views/public/News.vue')
const Products = () => import('../views/public/Products.vue')
const Login = () => import('../views/public/Login.vue')

// 员工系统页面
const Dashboard = () => import('../views/admin/Dashboard.vue')
const MonitoringSystem = () => import('../views/admin/MonitoringSystem.vue')
const EmployeeManagement = () => import('../views/admin/EmployeeManagement.vue')
const DeviceManagement = () => import('../views/admin/DeviceManagement.vue')

// 路由配置
const routes = [
  // 公共路由
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: false }
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    meta: { requiresAuth: false }
  },
  {
    path: '/news',
    name: 'News',
    component: News,
    meta: { requiresAuth: false }
  },
  {
    path: '/products',
    name: 'Products',
    component: Products,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  
  // 员工系统路由
  {
    path: '/admin',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/monitoring',
    name: 'MonitoringSystem',
    component: MonitoringSystem,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/employees',
    name: 'EmployeeManagement',
    component: EmployeeManagement,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/devices',
    name: 'DeviceManagement',
    component: DeviceManagement,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // 需要认证但未登录，重定向到登录页
    next({ name: 'Login' })
  } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    // 需要管理员权限但用户不是管理员
    next({ name: 'Dashboard' })
  } else {
    // 其他情况正常导航
    next()
  }
})

export default router 