import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    role: localStorage.getItem('role') || null,
    permissions: []
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.role === 'admin',
    isTechnician: (state) => state.role === 'technician',
    isBreeder: (state) => state.role === 'breeder',
    userPermissions: (state) => state.permissions
  },
  
  actions: {
    async login(credentials) {
      try {
        // 实际项目中，这里应该调用后端API进行认证
        const response = await axios.post('/api/auth/login', credentials)
        
        if (response.data.token) {
          this.setAuthData(response.data)
          return { success: true }
        }
        
        return { success: false, message: '登录失败，请检查用户名和密码' }
      } catch (error) {
        console.error('登录错误:', error)
        return { 
          success: false, 
          message: error.response?.data?.message || '登录时发生错误，请稍后再试' 
        }
      }
    },
    
    async fetchUserPermissions() {
      try {
        if (!this.token) return
        
        const response = await axios.get('/api/auth/permissions', {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        
        this.permissions = response.data.permissions
      } catch (error) {
        console.error('获取权限错误:', error)
      }
    },
    
    setAuthData(data) {
      this.token = data.token
      this.user = data.user
      this.role = data.role
      
      // 保存到本地存储
      localStorage.setItem('token', data.token)
      localStorage.setItem('role', data.role)
      
      // 设置axios默认头部
      axios.defaults.headers.common['Authorization'] = `Bearer ${data.token}`
      
      // 获取用户权限
      this.fetchUserPermissions()
    },
    
    logout() {
      this.user = null
      this.token = null
      this.role = null
      this.permissions = []
      
      // 清除本地存储
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      
      // 清除axios默认头部
      delete axios.defaults.headers.common['Authorization']
    }
  }
}) 