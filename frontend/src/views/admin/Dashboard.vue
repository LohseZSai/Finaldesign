<template>
  <div class="dashboard-page">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="250px" class="sidebar">
        <div class="logo-container">
          <img src="@/assets/logo.svg" alt="泓泰生物科技" class="logo" />
          <h2>智能养殖管理系统</h2>
        </div>
        
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          router
          background-color="#001529"
          text-color="#fff"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/admin">
            <el-icon><HomeFilled /></el-icon>
            <span>控制台</span>
          </el-menu-item>
          
          <el-menu-item index="/admin/monitoring">
            <el-icon><Monitor /></el-icon>
            <span>生产监控</span>
          </el-menu-item>
          
          <el-sub-menu index="data">
            <template #title>
              <el-icon><DataLine /></el-icon>
              <span>数据分析</span>
            </template>
            <el-menu-item index="/admin/data/environment">环境数据</el-menu-item>
            <el-menu-item index="/admin/data/production">生产数据</el-menu-item>
            <el-menu-item index="/admin/data/reports">报表中心</el-menu-item>
          </el-sub-menu>
          
          <el-menu-item index="/admin/devices">
            <el-icon><Connection /></el-icon>
            <span>设备管理</span>
          </el-menu-item>
          
          <el-menu-item v-if="isAdmin" index="/admin/employees">
            <el-icon><User /></el-icon>
            <span>员工管理</span>
          </el-menu-item>
          
          <el-menu-item index="/admin/settings">
            <el-icon><Setting /></el-icon>
            <span>系统设置</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区 -->
      <el-container>
        <!-- 顶部导航 -->
        <el-header class="header">
          <div class="header-left">
            <el-button
              type="text"
              :icon="isCollapse ? 'Expand' : 'Fold'"
              @click="toggleSidebar"
              class="toggle-button"
            />
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item>管理控制台</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          
          <div class="header-right">
            <el-badge :value="notificationsCount" class="notification-badge" v-if="notificationsCount">
              <el-button type="text" :icon="Bell" @click="showNotifications" />
            </el-badge>
            
            <el-dropdown trigger="click" @command="handleCommand">
              <div class="user-dropdown">
                <el-avatar :size="32" :src="userAvatar">{{ userInitials }}</el-avatar>
                <span class="username">{{ userName }}</span>
                <el-icon><ArrowDown /></el-icon>
              </div>
              
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                  <el-dropdown-item command="settings">账号设置</el-dropdown-item>
                  <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <!-- 主内容 -->
        <el-main class="main-content">
          <div class="dashboard-header">
            <h1>欢迎回来，{{ userName }}</h1>
            <p>{{ currentDate }}</p>
          </div>
          
          <!-- 数据概览卡片 -->
          <el-row :gutter="20" class="dashboard-cards">
            <el-col :xs="24" :sm="12" :md="6" v-for="(card, index) in overviewCards" :key="index">
              <el-card shadow="hover" class="overview-card" :body-style="{ padding: '20px' }">
                <div class="card-content">
                  <el-icon :size="40" :color="card.color">
                    <component :is="card.icon"></component>
                  </el-icon>
                  <div class="card-info">
                    <div class="card-value">{{ card.value }}</div>
                    <div class="card-label">{{ card.label }}</div>
                  </div>
                </div>
                <div class="card-footer">
                  <span :style="{ color: card.trend > 0 ? '#67C23A' : '#F56C6C' }">
                    <el-icon>
                      <component :is="card.trend > 0 ? 'ArrowUp' : 'ArrowDown'"></component>
                    </el-icon>
                    {{ Math.abs(card.trend) }}%
                  </span>
                  <span class="trend-label">较上周</span>
                </div>
              </el-card>
            </el-col>
          </el-row>
          
          <!-- 图表区域 -->
          <el-row :gutter="20" class="dashboard-charts">
            <el-col :xs="24" :lg="16">
              <el-card shadow="hover" class="chart-card">
                <template #header>
                  <div class="chart-header">
                    <h3>环境参数趋势</h3>
                    <el-radio-group v-model="environmentTimeRange" size="small">
                      <el-radio-button label="day">今日</el-radio-button>
                      <el-radio-button label="week">本周</el-radio-button>
                      <el-radio-button label="month">本月</el-radio-button>
                    </el-radio-group>
                  </div>
                </template>
                <div class="chart-container" ref="environmentChart"></div>
              </el-card>
            </el-col>
            
            <el-col :xs="24" :lg="8">
              <el-card shadow="hover" class="chart-card">
                <template #header>
                  <div class="chart-header">
                    <h3>猪群健康状态</h3>
                  </div>
                </template>
                <div class="chart-container" ref="healthChart"></div>
              </el-card>
            </el-col>
          </el-row>
          
          <!-- 最近告警和任务 -->
          <el-row :gutter="20" class="dashboard-tables">
            <el-col :xs="24" :lg="12">
              <el-card shadow="hover" class="table-card">
                <template #header>
                  <div class="card-header">
                    <h3>最近告警</h3>
                    <el-button type="text" @click="viewAllAlerts">查看全部</el-button>
                  </div>
                </template>
                <el-table :data="recentAlerts" style="width: 100%" :max-height="300">
                  <el-table-column prop="time" label="时间" width="180" />
                  <el-table-column prop="type" label="类型">
                    <template #default="scope">
                      <el-tag :type="getAlertTypeTag(scope.row.type)">
                        {{ scope.row.type }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="message" label="内容" />
                  <el-table-column label="操作" width="100">
                    <template #default="scope">
                      <el-button
                        type="text"
                        size="small"
                        @click="handleAlertAction(scope.row)"
                      >
                        处理
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </el-col>
            
            <el-col :xs="24" :lg="12">
              <el-card shadow="hover" class="table-card">
                <template #header>
                  <div class="card-header">
                    <h3>待办任务</h3>
                    <el-button type="text" @click="viewAllTasks">查看全部</el-button>
                  </div>
                </template>
                <el-table :data="recentTasks" style="width: 100%" :max-height="300">
                  <el-table-column prop="deadline" label="截止日期" width="180" />
                  <el-table-column prop="title" label="任务名称" />
                  <el-table-column prop="priority" label="优先级" width="100">
                    <template #default="scope">
                      <el-tag :type="getTaskPriorityTag(scope.row.priority)">
                        {{ scope.row.priority }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column label="状态" width="100">
                    <template #default="scope">
                      <el-switch
                        v-model="scope.row.completed"
                        @change="handleTaskStatusChange(scope.row)"
                      />
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </el-col>
          </el-row>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ref, onMounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useMonitoringStore } from '@/store/monitoring'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as echarts from 'echarts'

export default {
  name: 'DashboardPage',
  
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const monitoringStore = useMonitoringStore()
    
    // 侧边栏状态
    const isCollapse = ref(false)
    const activeMenu = ref('/admin')
    
    // 用户信息
    const userName = computed(() => authStore.user?.name || '用户')
    const userAvatar = computed(() => authStore.user?.avatar || '')
    const userInitials = computed(() => {
      const name = authStore.user?.name || ''
      return name.substring(0, 1).toUpperCase()
    })
    const isAdmin = computed(() => authStore.isAdmin)
    
    // 当前日期
    const currentDate = computed(() => {
      const now = new Date()
      return now.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      })
    })
    
    // 通知数量
    const notificationsCount = ref(3)
    
    // 环境数据时间范围
    const environmentTimeRange = ref('day')
    
    // 图表引用
    const environmentChart = ref(null)
    const healthChart = ref(null)
    
    // 数据概览卡片
    const overviewCards = ref([
      {
        icon: 'Pig',
        color: '#409EFF',
        label: '存栏数量',
        value: '1,256',
        trend: 5.2
      },
      {
        icon: 'Odometer',
        color: '#67C23A',
        label: '日均增重',
        value: '0.85kg',
        trend: 3.1
      },
      {
        icon: 'Warning',
        color: '#E6A23C',
        label: '活跃告警',
        value: '3',
        trend: -12.5
      },
      {
        icon: 'Cpu',
        color: '#F56C6C',
        label: '设备在线率',
        value: '98.5%',
        trend: 0.8
      }
    ])
    
    // 最近告警
    const recentAlerts = ref([
      {
        id: 1,
        time: '2025-03-15 08:23',
        type: '温度异常',
        message: '3号猪舍温度过高 (32.5°C)',
        status: 'active'
      },
      {
        id: 2,
        time: '2025-03-15 06:12',
        type: '设备离线',
        message: '饲喂机#2离线超过30分钟',
        status: 'active'
      },
      {
        id: 3,
        time: '2025-03-14 23:45',
        type: '湿度异常',
        message: '1号猪舍湿度过低 (35%)',
        status: 'active'
      }
    ])
    
    // 待办任务
    const recentTasks = ref([
      {
        id: 1,
        title: '更换1号猪舍过滤器',
        deadline: '2025-03-16',
        priority: '高',
        completed: false
      },
      {
        id: 2,
        title: '检查饲喂机运行状态',
        deadline: '2025-03-15',
        priority: '中',
        completed: false
      },
      {
        id: 3,
        title: '更新疫苗接种记录',
        deadline: '2025-03-17',
        priority: '低',
        completed: true
      },
      {
        id: 4,
        title: '清理排污系统',
        deadline: '2025-03-18',
        priority: '中',
        completed: false
      }
    ])
    
    // 方法
    const toggleSidebar = () => {
      isCollapse.value = !isCollapse.value
    }
    
    const handleCommand = (command) => {
      if (command === 'logout') {
        ElMessageBox.confirm('确定要退出登录吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          authStore.logout()
          router.push('/')
          ElMessage.success('已成功退出登录')
        }).catch(() => {})
      } else if (command === 'profile') {
        router.push('/admin/profile')
      } else if (command === 'settings') {
        router.push('/admin/settings')
      }
    }
    
    const showNotifications = () => {
      // 显示通知面板
      ElMessage.info('通知功能开发中')
    }
    
    const getAlertTypeTag = (type) => {
      const typeMap = {
        '温度异常': 'danger',
        '湿度异常': 'warning',
        '设备离线': 'info'
      }
      return typeMap[type] || 'info'
    }
    
    const getTaskPriorityTag = (priority) => {
      const priorityMap = {
        '高': 'danger',
        '中': 'warning',
        '低': 'info'
      }
      return priorityMap[priority] || 'info'
    }
    
    const handleAlertAction = (alert) => {
      ElMessageBox.confirm(`确定要处理"${alert.message}"告警吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 处理告警逻辑
        monitoringStore.acknowledgeAlert(alert.id)
        ElMessage.success('告警已标记为已处理')
      }).catch(() => {})
    }
    
    const handleTaskStatusChange = (task) => {
      ElMessage.success(`任务"${task.title}"状态已更新`)
    }
    
    const viewAllAlerts = () => {
      router.push('/admin/monitoring')
    }
    
    const viewAllTasks = () => {
      router.push('/admin/tasks')
    }
    
    // 初始化图表
    const initCharts = () => {
      // 环境参数趋势图
      if (environmentChart.value) {
        const chart = echarts.init(environmentChart.value)
        
        const option = {
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['温度', '湿度', '氨气浓度']
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00']
          },
          yAxis: [
            {
              type: 'value',
              name: '温度 (°C) / 湿度 (%)',
              position: 'left'
            },
            {
              type: 'value',
              name: '氨气 (ppm)',
              position: 'right'
            }
          ],
          series: [
            {
              name: '温度',
              type: 'line',
              data: [24, 23, 22, 25, 27, 28, 26, 25],
              smooth: true,
              lineStyle: {
                width: 3,
                color: '#F56C6C'
              }
            },
            {
              name: '湿度',
              type: 'line',
              data: [65, 68, 70, 68, 60, 55, 58, 62],
              smooth: true,
              lineStyle: {
                width: 3,
                color: '#409EFF'
              }
            },
            {
              name: '氨气浓度',
              type: 'line',
              yAxisIndex: 1,
              data: [5, 4, 4, 6, 8, 9, 7, 6],
              smooth: true,
              lineStyle: {
                width: 3,
                color: '#E6A23C'
              }
            }
          ]
        }
        
        chart.setOption(option)
        
        // 响应窗口大小变化
        window.addEventListener('resize', () => {
          chart.resize()
        })
      }
      
      // 猪群健康状态图
      if (healthChart.value) {
        const chart = echarts.init(healthChart.value)
        
        const option = {
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 10,
            data: ['健康', '需观察', '生病']
          },
          series: [
            {
              name: '猪群健康状态',
              type: 'pie',
              radius: ['50%', '70%'],
              avoidLabelOverlap: false,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
              label: {
                show: false,
                position: 'center'
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: '18',
                  fontWeight: 'bold'
                }
              },
              labelLine: {
                show: false
              },
              data: [
                { value: 1150, name: '健康', itemStyle: { color: '#67C23A' } },
                { value: 85, name: '需观察', itemStyle: { color: '#E6A23C' } },
                { value: 21, name: '生病', itemStyle: { color: '#F56C6C' } }
              ]
            }
          ]
        }
        
        chart.setOption(option)
        
        // 响应窗口大小变化
        window.addEventListener('resize', () => {
          chart.resize()
        })
      }
    }
    
    // 生命周期钩子
    onMounted(async () => {
      // 获取数据
      try {
        await monitoringStore.fetchAllMonitoringData()
      } catch (error) {
        console.error('获取监控数据错误:', error)
      }
      
      // 初始化图表
      nextTick(() => {
        initCharts()
      })
    })
    
    return {
      isCollapse,
      activeMenu,
      userName,
      userAvatar,
      userInitials,
      isAdmin,
      currentDate,
      notificationsCount,
      environmentTimeRange,
      environmentChart,
      healthChart,
      overviewCards,
      recentAlerts,
      recentTasks,
      toggleSidebar,
      handleCommand,
      showNotifications,
      getAlertTypeTag,
      getTaskPriorityTag,
      handleAlertAction,
      handleTaskStatusChange,
      viewAllAlerts,
      viewAllTasks
    }
  }
}
</script>

<style scoped>
.dashboard-page {
  height: 100vh;
  overflow: hidden;
}

/* 侧边栏样式 */
.sidebar {
  background-color: #001529;
  color: white;
  height: 100vh;
  overflow-y: auto;
  transition: width 0.3s;
}

.logo-container {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  height: 40px;
  margin-bottom: 10px;
}

.logo-container h2 {
  font-size: 1.2rem;
  margin: 0;
  color: white;
}

.sidebar-menu {
  border-right: none;
}

/* 头部样式 */
.header {
  background-color: white;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.toggle-button {
  margin-right: 15px;
}

.header-right {
  display: flex;
  align-items: center;
}

.notification-badge {
  margin-right: 20px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.username {
  margin: 0 10px;
}

/* 主内容区样式 */
.main-content {
  padding: 20px;
  height: calc(100vh - 60px);
  overflow-y: auto;
  background-color: #f5f7fa;
}

.dashboard-header {
  margin-bottom: 20px;
}

.dashboard-header h1 {
  margin: 0 0 5px 0;
  font-size: 1.8rem;
  color: #333;
}

.dashboard-header p {
  margin: 0;
  color: #666;
}

/* 卡片样式 */
.dashboard-cards {
  margin-bottom: 20px;
}

.overview-card {
  height: 100%;
  transition: transform 0.3s;
}

.overview-card:hover {
  transform: translateY(-5px);
}

.card-content {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.card-info {
  margin-left: 15px;
}

.card-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  line-height: 1;
}

.card-label {
  color: #999;
  margin-top: 5px;
}

.card-footer {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
}

.trend-label {
  margin-left: 5px;
  color: #999;
}

/* 图表样式 */
.dashboard-charts {
  margin-bottom: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.chart-container {
  height: 300px;
}

/* 表格卡片样式 */
.dashboard-tables {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    z-index: 1000;
  }
  
  .main-content {
    padding: 15px;
  }
  
  .dashboard-header h1 {
    font-size: 1.5rem;
  }
  
  .card-value {
    font-size: 1.5rem;
  }
}
</style> 