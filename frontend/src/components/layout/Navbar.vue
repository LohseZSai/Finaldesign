<template>
  <el-menu
    :default-active="activeIndex"
    class="navbar"
    mode="horizontal"
    :ellipsis="false"
    router
    @select="handleSelect"
  >
    <div class="logo-container">
      <router-link to="/">
        <img src="@/assets/logo.svg" alt="泓泰生物科技" class="logo" />
      </router-link>
    </div>
    
    <div class="flex-grow" />
    
    <!-- 公共导航链接 -->
    <el-menu-item index="/">首页</el-menu-item>
    <el-menu-item index="/products">产品服务</el-menu-item>
    <el-menu-item index="/news">新闻动态</el-menu-item>
    <el-menu-item index="/about">关于我们</el-menu-item>
    
    <!-- 登录/员工入口 -->
    <el-menu-item v-if="!isAuthenticated" index="/login">
      <el-button type="primary" size="small">员工登录</el-button>
    </el-menu-item>
    
    <!-- 已登录用户下拉菜单 -->
    <el-sub-menu v-else index="user">
      <template #title>
        <el-avatar :size="32" :src="userAvatar">
          {{ userInitials }}
        </el-avatar>
        <span class="ml-2">{{ userName }}</span>
      </template>
      
      <el-menu-item index="/admin">管理控制台</el-menu-item>
      <el-menu-item index="/admin/monitoring">生产监控</el-menu-item>
      <el-menu-item v-if="isAdmin" index="/admin/employees">员工管理</el-menu-item>
      <el-menu-item index="/admin/devices">设备管理</el-menu-item>
      <el-menu-item @click="handleLogout">退出登录</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

export default {
  name: 'Navbar',
  
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    
    const activeIndex = ref(route.path)
    
    // 计算属性
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const isAdmin = computed(() => authStore.isAdmin)
    const userName = computed(() => authStore.user?.name || '用户')
    const userAvatar = computed(() => authStore.user?.avatar || '')
    const userInitials = computed(() => {
      const name = authStore.user?.name || ''
      return name.substring(0, 1).toUpperCase()
    })
    
    // 方法
    const handleSelect = (key) => {
      activeIndex.value = key
    }
    
    const handleLogout = async () => {
      authStore.logout()
      router.push('/')
    }
    
    return {
      activeIndex,
      isAuthenticated,
      isAdmin,
      userName,
      userAvatar,
      userInitials,
      handleSelect,
      handleLogout
    }
  }
}
</script>

<style scoped>
.navbar {
  height: 64px;
  padding: 0 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.logo {
  height: 40px;
}

.flex-grow {
  flex-grow: 1;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .navbar {
    padding: 0 10px;
  }
  
  .logo {
    height: 32px;
  }
}
</style> 