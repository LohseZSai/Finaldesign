<template>
  <div class="monitoring-page">
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
              <el-breadcrumb-item :to="{ path: '/admin' }">控制台</el-breadcrumb-item>
              <el-breadcrumb-item>生产监控</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          
          <div class="header-right">
            <el-badge :value="activeAlertsCount" class="notification-badge" v-if="activeAlertsCount">
              <el-button type="text" :icon="Bell" @click="showAlerts" />
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
          <div class="monitoring-header">
            <h1>生产监控中心</h1>
            <div class="monitoring-actions">
              <span class="last-updated">最后更新: {{ lastUpdatedTime }}</span>
              <el-button type="primary" :loading="isRefreshing" @click="refreshData">
                <el-icon><Refresh /></el-icon> 刷新数据
              </el-button>
            </div>
          </div>
          
          <!-- 环境监控卡片 -->
          <el-row :gutter="20" class="monitoring-section">
            <el-col :span="24">
              <h2 class="section-title">
                <el-icon><Cloudy /></el-icon> 环境监控
              </h2>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="(area, index) in monitoringAreas" :key="index">
              <el-card shadow="hover" class="env-card" :body-style="{ padding: '0' }">
                <div class="env-card-header">
                  <h3>{{ area.name }}</h3>
                  <el-tag :type="getAreaStatusType(area.status)">{{ area.status }}</el-tag>
                </div>
                
                <div class="env-card-body">
                  <div class="env-param">
                    <div class="param-icon">
                      <el-icon :color="getParamColor(area.temperature.value, 'temperature')"><Sunny /></el-icon>
                    </div>
                    <div class="param-info">
                      <div class="param-label">温度</div>
                      <div class="param-value" :class="getParamClass(area.temperature.value, 'temperature')">
                        {{ area.temperature.value }}°C
                      </div>
                    </div>
                    <div class="param-trend">
                      <el-icon v-if="area.temperature.trend > 0"><ArrowUp /></el-icon>
                      <el-icon v-else-if="area.temperature.trend < 0"><ArrowDown /></el-icon>
                      <el-icon v-else><DArrowRight /></el-icon>
                    </div>
                  </div>
                  
                  <div class="env-param">
                    <div class="param-icon">
                      <el-icon :color="getParamColor(area.humidity.value, 'humidity')"><Umbrella /></el-icon>
                    </div>
                    <div class="param-info">
                      <div class="param-label">湿度</div>
                      <div class="param-value" :class="getParamClass(area.humidity.value, 'humidity')">
                        {{ area.humidity.value }}%
                      </div>
                    </div>
                    <div class="param-trend">
                      <el-icon v-if="area.humidity.trend > 0"><ArrowUp /></el-icon>
                      <el-icon v-else-if="area.humidity.trend < 0"><ArrowDown /></el-icon>
                      <el-icon v-else><DArrowRight /></el-icon>
                    </div>
                  </div>
                  
                  <div class="env-param">
                    <div class="param-icon">
                      <el-icon :color="getParamColor(area.ammonia.value, 'ammonia')"><Aim /></el-icon>
                    </div>
                    <div class="param-info">
                      <div class="param-label">氨气</div>
                      <div class="param-value" :class="getParamClass(area.ammonia.value, 'ammonia')">
                        {{ area.ammonia.value }} ppm
                      </div>
                    </div>
                    <div class="param-trend">
                      <el-icon v-if="area.ammonia.trend > 0"><ArrowUp /></el-icon>
                      <el-icon v-else-if="area.ammonia.trend < 0"><ArrowDown /></el-icon>
                      <el-icon v-else><DArrowRight /></el-icon>
                    </div>
                  </div>
                </div>
                
                <div class="env-card-footer">
                  <el-button type="text" @click="viewAreaDetails(area)">查看详情</el-button>
                  <el-button type="text" @click="viewAreaHistory(area)">历史数据</el-button>
                </div>
              </el-card>
            </el-col>
          </el-row>
          
          <!-- 猪群监控 -->
          <el-row :gutter="20" class="monitoring-section">
            <el-col :span="24">
              <h2 class="section-title">
                <el-icon><Pig /></el-icon> 猪群监控
              </h2>
            </el-col>
            
            <el-col :xs="24" :lg="12">
              <el-card shadow="hover" class="chart-card">
                <template #header>
                  <div class="chart-header">
                    <h3>猪群分布</h3>
                    <el-select v-model="pigDataType" size="small" @change="updatePigChart">
                      <el-option label="按体重分布" value="weight" />
                      <el-option label="按年龄分布" value="age" />
                      <el-option label="按健康状态" value="health" />
                    </el-select>
                  </div>
                </template>
                <div class="chart-container" ref="pigDistributionChart"></div>
              </el-card>
            </el-col>
            
            <el-col :xs="24" :lg="12">
              <el-card shadow="hover" class="pig-status-card">
                <template #header>
                  <div class="card-header">
                    <h3>猪群状态概览</h3>
                  </div>
                </template>
                <div class="pig-status-content">
                  <div class="status-item">
                    <div class="status-label">总存栏数</div>
                    <div class="status-value">{{ pigStatus.totalCount }}</div>
                    <div class="status-trend" :class="{ 'up': pigStatus.countTrend > 0, 'down': pigStatus.countTrend < 0 }">
                      <el-icon v-if="pigStatus.countTrend > 0"><ArrowUp /></el-icon>
                      <el-icon v-else-if="pigStatus.countTrend < 0"><ArrowDown /></el-icon>
                      {{ Math.abs(pigStatus.countTrend) }}%
                    </div>
                  </div>
                  
                  <div class="status-item">
                    <div class="status-label">平均体重</div>
                    <div class="status-value">{{ pigStatus.avgWeight }} kg</div>
                    <div class="status-trend" :class="{ 'up': pigStatus.weightTrend > 0, 'down': pigStatus.weightTrend < 0 }">
                      <el-icon v-if="pigStatus.weightTrend > 0"><ArrowUp /></el-icon>
                      <el-icon v-else-if="pigStatus.weightTrend < 0"><ArrowDown /></el-icon>
                      {{ Math.abs(pigStatus.weightTrend) }}%
                    </div>
                  </div>
                  
                  <div class="status-item">
                    <div class="status-label">日均增重</div>
                    <div class="status-value">{{ pigStatus.dailyGain }} kg</div>
                    <div class="status-trend" :class="{ 'up': pigStatus.gainTrend > 0, 'down': pigStatus.gainTrend < 0 }">
                      <el-icon v-if="pigStatus.gainTrend > 0"><ArrowUp /></el-icon>
                      <el-icon v-else-if="pigStatus.gainTrend < 0"><ArrowDown /></el-icon>
                      {{ Math.abs(pigStatus.gainTrend) }}%
                    </div>
                  </div>
                  
                  <div class="status-item">
                    <div class="status-label">健康率</div>
                    <div class="status-value">{{ pigStatus.healthRate }}%</div>
                    <div class="status-trend" :class="{ 'up': pigStatus.healthTrend > 0, 'down': pigStatus.healthTrend < 0 }">
                      <el-icon v-if="pigStatus.healthTrend > 0"><ArrowUp /></el-icon>
                      <el-icon v-else-if="pigStatus.healthTrend < 0"><ArrowDown /></el-icon>
                      {{ Math.abs(pigStatus.healthTrend) }}%
                    </div>
                  </div>
                </div>
                
                <el-divider />
                
                <div class="pig-actions">
                  <el-button type="primary" @click="viewPigDetails">查看详细数据</el-button>
                  <el-button @click="exportPigData">导出数据</el-button>
                </div>
              </el-card>
            </el-col>
          </el-row>
          
          <!-- 饲喂监控 -->
          <el-row :gutter="20" class="monitoring-section">
            <el-col :span="24">
              <h2 class="section-title">
                <el-icon><Food /></el-icon> 饲喂监控
              </h2>
            </el-col>
            
            <el-col :xs="24" :lg="12">
              <el-card shadow="hover" class="chart-card">
                <template #header>
                  <div class="chart-header">
                    <h3>饲料消耗趋势</h3>
                    <el-radio-group v-model="feedTimeRange" size="small" @change="updateFeedChart">
                      <el-radio-button label="week">本周</el-radio-button>
                      <el-radio-button label="month">本月</el-radio-button>
                      <el-radio-button label="quarter">本季度</el-radio-button>
                    </el-radio-group>
                  </div>
                </template>
                <div class="chart-container" ref="feedConsumptionChart"></div>
              </el-card>
            </el-col>
            
            <el-col :xs="24" :lg="12">
              <el-card shadow="hover" class="feed-status-card">
                <template #header>
                  <div class="card-header">
                    <h3>饲料库存状态</h3>
                  </div>
                </template>
                <div class="feed-status-content">
                  <div v-for="(feed, index) in feedStocks" :key="index" class="feed-item">
                    <div class="feed-info">
                      <div class="feed-name">{{ feed.name }}</div>
                      <div class="feed-stock-info">
                        <span>库存: {{ feed.current }}kg / {{ feed.capacity }}kg</span>
                        <span :class="getFeedStockClass(feed)">
                          ({{ Math.round(feed.current / feed.capacity * 100) }}%)
                        </span>
                      </div>
                    </div>
                    
                    <el-progress
                      :percentage="Math.round(feed.current / feed.capacity * 100)"
                      :status="getFeedStockStatus(feed)"
                      :stroke-width="15"
                    />
                    
                    <div class="feed-actions">
                      <span class="feed-estimate">预计可用: {{ feed.estimatedDays }}天</span>
                      <el-button
                        v-if="feed.current / feed.capacity < 0.2"
                        type="warning"
                        size="small"
                        @click="orderFeed(feed)"
                      >
                        补充库存
                      </el-button>
                    </div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
          
          <!-- 视频监控 -->
          <el-row :gutter="20" class="monitoring-section">
            <el-col :span="24">
              <h2 class="section-title">
                <el-icon><VideoCamera /></el-icon> 视频监控
              </h2>
            </el-col>
            
            <el-col :xs="24" :sm="12" :lg="8" v-for="(camera, index) in cameraStreams" :key="index">
              <el-card shadow="hover" class="camera-card">
                <div class="camera-header">
                  <h3>{{ camera.name }}</h3>
                  <el-tag :type="camera.status === 'online' ? 'success' : 'danger'">
                    {{ camera.status === 'online' ? '在线' : '离线' }}
                  </el-tag>
                </div>
                
                <div class="camera-stream" v-if="camera.status === 'online'">
                  <img :src="camera.streamUrl" alt="摄像头画面" />
                </div>
                <div class="camera-offline" v-else>
                  <el-icon :size="48"><VideoPlay /></el-icon>
                  <p>摄像头离线</p>
                </div>
                
                <div class="camera-actions">
                  <el-button-group>
                    <el-button type="primary" :disabled="camera.status !== 'online'" @click="viewFullscreen(camera)">
                      <el-icon><FullScreen /></el-icon>
                    </el-button>
                    <el-button type="primary" :disabled="camera.status !== 'online'" @click="viewRecordings(camera)">
                      <el-icon><VideoPlay /></el-icon>
                    </el-button>
                    <el-button type="primary" @click="cameraSettings(camera)">
                      <el-icon><Setting /></el-icon>
                    </el-button>
                  </el-button-group>
                </div>
              </el-card>
            </el-col>
          </el-row>
          
          <!-- 告警信息 -->
          <el-row :gutter="20" class="monitoring-section">
            <el-col :span="24">
              <h2 class="section-title">
                <el-icon><Warning /></el-icon> 告警信息
                <el-badge :value="activeAlertsCount" class="alert-badge" v-if="activeAlertsCount" />
              </h2>
            </el-col>
            
            <el-col :span="24">
              <el-card shadow="hover" class="alerts-card">
                <template #header>
                  <div class="card-header">
                    <div class="alert-tabs">
                      <el-radio-group v-model="alertsTab" size="small">
                        <el-radio-button label="active">活跃告警 ({{ activeAlertsCount }})</el-radio-button>
                        <el-radio-button label="history">历史告警</el-radio-button>
                      </el-radio-group>
                    </div>
                    
                    <div class="alert-actions">
                      <el-button
                        v-if="alertsTab === 'active' && activeAlertsCount > 0"
                        type="warning"
                        size="small"
                        @click="acknowledgeAllAlerts"
                      >
                        全部确认
                      </el-button>
                      <el-button type="primary" size="small" @click="exportAlerts">
                        导出
                      </el-button>
                    </div>
                  </div>
                </template>
                
                <el-table
                  :data="alertsTab === 'active' ? activeAlerts : historyAlerts"
                  style="width: 100%"
                  :max-height="400"
                  v-loading="alertsLoading"
                >
                  <el-table-column prop="time" label="时间" width="180" sortable />
                  <el-table-column prop="area" label="区域" width="150" />
                  <el-table-column prop="type" label="类型" width="120">
                    <template #default="scope">
                      <el-tag :type="getAlertTypeTag(scope.row.type)">
                        {{ scope.row.type }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="level" label="级别" width="100">
                    <template #default="scope">
                      <el-tag :type="getAlertLevelTag(scope.row.level)">
                        {{ scope.row.level }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="message" label="内容" />
                  <el-table-column label="操作" width="180" fixed="right">
                    <template #default="scope">
                      <el-button
                        v-if="alertsTab === 'active'"
                        type="primary"
                        size="small"
                        @click="acknowledgeAlert(scope.row)"
                      >
                        确认
                      </el-button>
                      <el-button
                        type="info"
                        size="small"
                        @click="viewAlertDetails(scope.row)"
                      >
                        详情
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
                
                <div class="pagination-container">
                  <el-pagination
                    v-model:current-page="alertsPage"
                    v-model:page-size="alertsPageSize"
                    :page-sizes="[10, 20, 50, 100]"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="alertsTab === 'active' ? totalActiveAlerts : totalHistoryAlerts"
                    @size-change="handleAlertsPageSizeChange"
                    @current-change="handleAlertsPageChange"
                  />
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-main>
      </el-container>
    </el-container>
    
    <!-- 告警详情对话框 -->
    <el-dialog
      v-model="alertDialogVisible"
      title="告警详情"
      width="600px"
      destroy-on-close
    >
      <div v-if="selectedAlert" class="alert-detail">
        <div class="alert-detail-item">
          <span class="detail-label">告警ID:</span>
          <span class="detail-value">{{ selectedAlert.id }}</span>
        </div>
        <div class="alert-detail-item">
          <span class="detail-label">时间:</span>
          <span class="detail-value">{{ selectedAlert.time }}</span>
        </div>
        <div class="alert-detail-item">
          <span class="detail-label">区域:</span>
          <span class="detail-value">{{ selectedAlert.area }}</span>
        </div>
        <div class="alert-detail-item">
          <span class="detail-label">类型:</span>
          <span class="detail-value">
            <el-tag :type="getAlertTypeTag(selectedAlert.type)">
              {{ selectedAlert.type }}
            </el-tag>
          </span>
        </div>
        <div class="alert-detail-item">
          <span class="detail-label">级别:</span>
          <span class="detail-value">
            <el-tag :type="getAlertLevelTag(selectedAlert.level)">
              {{ selectedAlert.level }}
            </el-tag>
          </span>
        </div>
        <div class="alert-detail-item">
          <span class="detail-label">内容:</span>
          <span class="detail-value">{{ selectedAlert.message }}</span>
        </div>
        <div class="alert-detail-item">
          <span class="detail-label">详细描述:</span>
          <span class="detail-value">{{ selectedAlert.description }}</span>
        </div>
        <div class="alert-detail-item" v-if="selectedAlert.parameters">
          <span class="detail-label">相关参数:</span>
          <div class="detail-value parameters-list">
            <div v-for="(value, key) in selectedAlert.parameters" :key="key" class="parameter-item">
              <span class="parameter-name">{{ key }}:</span>
              <span class="parameter-value">{{ value }}</span>
            </div>
          </div>
        </div>
        <div class="alert-detail-item" v-if="alertsTab === 'history' && selectedAlert.resolvedBy">
          <span class="detail-label">处理人:</span>
          <span class="detail-value">{{ selectedAlert.resolvedBy }}</span>
        </div>
        <div class="alert-detail-item" v-if="alertsTab === 'history' && selectedAlert.resolvedTime">
          <span class="detail-label">处理时间:</span>
          <span class="detail-value">{{ selectedAlert.resolvedTime }}</span>
        </div>
        <div class="alert-detail-item" v-if="alertsTab === 'history' && selectedAlert.resolution">
          <span class="detail-label">处理方式:</span>
          <span class="detail-value">{{ selectedAlert.resolution }}</span>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="alertDialogVisible = false">关闭</el-button>
          <el-button
            v-if="alertsTab === 'active' && selectedAlert"
            type="primary"
            @click="acknowledgeAlertFromDialog"
          >
            确认告警
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, nextTick, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useMonitoringStore } from '@/store/monitoring'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as echarts from 'echarts'

export default {
  name: 'MonitoringSystemPage',
  
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const monitoringStore = useMonitoringStore()
    
    // 侧边栏状态
    const isCollapse = ref(false)
    const activeMenu = ref('/admin/monitoring')
    
    // 用户信息
    const userName = computed(() => authStore.user?.name || '用户')
    const userAvatar = computed(() => authStore.user?.avatar || '')
    const userInitials = computed(() => {
      const name = authStore.user?.name || ''
      return name.substring(0, 1).toUpperCase()
    })
    const isAdmin = computed(() => authStore.isAdmin)
    
    // 数据刷新状态
    const isRefreshing = ref(false)
    const lastUpdatedTime = ref(formatDateTime(new Date()))
    
    // 图表引用
    const pigDistributionChart = ref(null)
    const feedConsumptionChart = ref(null)
    let pigChart = null
    let feedChart = null
    
    // 猪群数据类型
    const pigDataType = ref('weight')
    
    // 饲料时间范围
    const feedTimeRange = ref('week')
    
    // 告警相关
    const alertsTab = ref('active')
    const alertsLoading = ref(false)
    const alertsPage = ref(1)
    const alertsPageSize = ref(10)
    const totalActiveAlerts = ref(0)
    const totalHistoryAlerts = ref(0)
    const alertDialogVisible = ref(false)
    const selectedAlert = ref(null)
    
    // 活跃告警数量
    const activeAlertsCount = computed(() => activeAlerts.value.length)
    
    // 监控区域数据
    const monitoringAreas = ref([
      {
        id: 1,
        name: '1号猪舍',
        status: '正常',
        temperature: { value: 25.6, trend: 0.5 },
        humidity: { value: 65, trend: -2 },
        ammonia: { value: 5, trend: 0 }
      },
      {
        id: 2,
        name: '2号猪舍',
        status: '正常',
        temperature: { value: 26.2, trend: 1.2 },
        humidity: { value: 62, trend: -1 },
        ammonia: { value: 6, trend: 0.5 }
      },
      {
        id: 3,
        name: '3号猪舍',
        status: '警告',
        temperature: { value: 29.8, trend: 3.5 },
        humidity: { value: 58, trend: -5 },
        ammonia: { value: 8, trend: 2 }
      },
      {
        id: 4,
        name: '4号猪舍',
        status: '正常',
        temperature: { value: 24.9, trend: -0.3 },
        humidity: { value: 68, trend: 2 },
        ammonia: { value: 4, trend: -1 }
      }
    ])
    
    // 猪群状态数据
    const pigStatus = reactive({
      totalCount: 1256,
      countTrend: 2.5,
      avgWeight: 78.3,
      weightTrend: 1.8,
      dailyGain: 0.85,
      gainTrend: 3.2,
      healthRate: 91.5,
      healthTrend: -0.5
    })
    
    // 饲料库存数据
    const feedStocks = ref([
      {
        id: 1,
        name: '标准饲料A',
        current: 2800,
        capacity: 5000,
        estimatedDays: 14
      },
      {
        id: 2,
        name: '生长促进饲料B',
        current: 1200,
        capacity: 3000,
        estimatedDays: 8
      },
      {
        id: 3,
        name: '营养强化饲料C',
        current: 450,
        capacity: 2000,
        estimatedDays: 4
      }
    ])
    
    // 摄像头数据
    const cameraStreams = ref([
      {
        id: 1,
        name: '1号猪舍-入口',
        status: 'online',
        streamUrl: 'https://example.com/stream1.jpg'
      },
      {
        id: 2,
        name: '1号猪舍-中部',
        status: 'online',
        streamUrl: 'https://example.com/stream2.jpg'
      },
      {
        id: 3,
        name: '2号猪舍-入口',
        status: 'online',
        streamUrl: 'https://example.com/stream3.jpg'
      },
      {
        id: 4,
        name: '3号猪舍-中部',
        status: 'offline',
        streamUrl: ''
      },
      {
        id: 5,
        name: '4号猪舍-入口',
        status: 'online',
        streamUrl: 'https://example.com/stream5.jpg'
      }
    ])
    
    // 告警数据
    const activeAlerts = ref([
      {
        id: 1,
        time: '2025-03-15 08:23:45',
        area: '3号猪舍',
        type: '温度异常',
        level: '警告',
        message: '温度过高 (29.8°C)',
        description: '3号猪舍温度持续30分钟超过29°C，已超过预设阈值(28°C)。',
        parameters: {
          '当前温度': '29.8°C',
          '阈值': '28°C',
          '持续时间': '30分钟'
        }
      },
      {
        id: 2,
        time: '2025-03-15 07:45:12',
        area: '2号猪舍',
        type: '设备异常',
        level: '一般',
        message: '饲喂机#2运行异常',
        description: '饲喂机#2运行时出现异常噪音，可能需要维护检查。',
        parameters: {
          '设备ID': 'FEEDER-002',
          '异常类型': '噪音异常',
          '上次维护': '2025-02-28'
        }
      },
      {
        id: 3,
        time: '2025-03-15 06:12:33',
        area: '全场',
        type: '系统警告',
        level: '一般',
        message: '数据备份延迟',
        description: '系统数据备份已延迟超过12小时，请检查备份服务状态。',
        parameters: {
          '上次备份': '2025-03-14 18:00:05',
          '延迟时间': '12小时12分钟',
          '影响服务': '历史数据查询'
        }
      }
    ])
    
    const historyAlerts = ref([
      {
        id: 101,
        time: '2025-03-14 14:23:45',
        area: '1号猪舍',
        type: '湿度异常',
        level: '警告',
        message: '湿度过低 (45%)',
        description: '1号猪舍湿度持续45分钟低于50%，已低于预设阈值(50%)。',
        parameters: {
          '当前湿度': '45%',
          '阈值': '50%',
          '持续时间': '45分钟'
        },
        resolvedBy: '张工程师',
        resolvedTime: '2025-03-14 15:10:22',
        resolution: '已调整通风系统，湿度恢复正常'
      },
      {
        id: 102,
        time: '2025-03-14 10:15:33',
        area: '4号猪舍',
        type: '氨气异常',
        level: '严重',
        message: '氨气浓度过高 (15ppm)',
        description: '4号猪舍氨气浓度达到15ppm，已超过危险阈值(10ppm)。',
        parameters: {
          '当前浓度': '15ppm',
          '阈值': '10ppm',
          '持续时间': '15分钟'
        },
        resolvedBy: '李主管',
        resolvedTime: '2025-03-14 11:05:18',
        resolution: '已增强通风并清理粪污，浓度已降至安全水平'
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
    
    const refreshData = async () => {
      try {
        isRefreshing.value = true
        await monitoringStore.fetchAllMonitoringData()
        lastUpdatedTime.value = formatDateTime(new Date())
        ElMessage.success('数据已刷新')
      } catch (error) {
        console.error('刷新数据错误:', error)
        ElMessage.error('刷新数据失败，请稍后再试')
      } finally {
        isRefreshing.value = false
      }
    }
    
    // 格式化日期时间
    function formatDateTime(date) {
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      })
    }
    
    // 环境参数相关方法
    const getAreaStatusType = (status) => {
      const statusMap = {
        '正常': 'success',
        '警告': 'warning',
        '异常': 'danger'
      }
      return statusMap[status] || 'info'
    }
    
    const getParamColor = (value, type) => {
      if (type === 'temperature') {
        if (value > 28) return '#F56C6C'
        if (value < 20) return '#409EFF'
        return '#67C23A'
      } else if (type === 'humidity') {
        if (value > 80) return '#F56C6C'
        if (value < 50) return '#E6A23C'
        return '#67C23A'
      } else if (type === 'ammonia') {
        if (value > 10) return '#F56C6C'
        if (value > 7) return '#E6A23C'
        return '#67C23A'
      }
      return '#909399'
    }
    
    const getParamClass = (value, type) => {
      if (type === 'temperature') {
        if (value > 28) return 'param-danger'
        if (value < 20) return 'param-warning'
        return 'param-normal'
      } else if (type === 'humidity') {
        if (value > 80) return 'param-danger'
        if (value < 50) return 'param-warning'
        return 'param-normal'
      } else if (type === 'ammonia') {
        if (value > 10) return 'param-danger'
        if (value > 7) return 'param-warning'
        return 'param-normal'
      }
      return 'param-normal'
    }
    
    const viewAreaDetails = (area) => {
      router.push(`/admin/monitoring/area/${area.id}`)
    }
    
    const viewAreaHistory = (area) => {
      router.push(`/admin/monitoring/area/${area.id}/history`)
    }
    
    // 猪群相关方法
    const viewPigDetails = () => {
      router.push('/admin/monitoring/pigs')
    }
    
    const exportPigData = () => {
      ElMessage.success('猪群数据导出功能开发中')
    }
    
    // 饲料相关方法
    const getFeedStockClass = (feed) => {
      const percentage = feed.current / feed.capacity * 100
      if (percentage < 20) return 'stock-danger'
      if (percentage < 40) return 'stock-warning'
      return 'stock-normal'
    }
    
    const getFeedStockStatus = (feed) => {
      const percentage = feed.current / feed.capacity * 100
      if (percentage < 20) return 'exception'
      if (percentage < 40) return 'warning'
      return 'success'
    }
    
    const orderFeed = (feed) => {
      ElMessageBox.confirm(`确定要为"${feed.name}"补充库存吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }).then(() => {
        ElMessage.success(`已创建"${feed.name}"的补充库存订单`)
      }).catch(() => {})
    }
    
    // 摄像头相关方法
    const viewFullscreen = (camera) => {
      ElMessage.info(`全屏查看${camera.name}功能开发中`)
    }
    
    const viewRecordings = (camera) => {
      router.push(`/admin/monitoring/camera/${camera.id}/recordings`)
    }
    
    const cameraSettings = (camera) => {
      router.push(`/admin/monitoring/camera/${camera.id}/settings`)
    }
    
    // 告警相关方法
    const getAlertTypeTag = (type) => {
      const typeMap = {
        '温度异常': 'danger',
        '湿度异常': 'warning',
        '氨气异常': 'danger',
        '设备异常': 'info',
        '系统警告': 'warning'
      }
      return typeMap[type] || 'info'
    }
    
    const getAlertLevelTag = (level) => {
      const levelMap = {
        '严重': 'danger',
        '警告': 'warning',
        '一般': 'info'
      }
      return levelMap[level] || 'info'
    }
    
    const showAlerts = () => {
      alertsTab.value = 'active'
      window.scrollTo({
        top: document.querySelector('.alerts-card').offsetTop - 80,
        behavior: 'smooth'
      })
    }
    
    const acknowledgeAlert = async (alert) => {
      try {
        await monitoringStore.acknowledgeAlert(alert.id)
        ElMessage.success(`已确认告警: ${alert.message}`)
        // 在实际应用中，这里应该重新获取告警列表
        activeAlerts.value = activeAlerts.value.filter(a => a.id !== alert.id)
      } catch (error) {
        ElMessage.error('确认告警失败，请稍后再试')
      }
    }
    
    const acknowledgeAllAlerts = async () => {
      ElMessageBox.confirm('确定要确认所有活跃告警吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          alertsLoading.value = true
          // 在实际应用中，这里应该调用批量确认API
          await new Promise(resolve => setTimeout(resolve, 1000))
          activeAlerts.value = []
          ElMessage.success('已确认所有告警')
        } catch (error) {
          ElMessage.error('确认告警失败，请稍后再试')
        } finally {
          alertsLoading.value = false
        }
      }).catch(() => {})
    }
    
    const viewAlertDetails = (alert) => {
      selectedAlert.value = alert
      alertDialogVisible.value = true
    }
    
    const acknowledgeAlertFromDialog = async () => {
      if (!selectedAlert.value) return
      
      try {
        await monitoringStore.acknowledgeAlert(selectedAlert.value.id)
        ElMessage.success(`已确认告警: ${selectedAlert.value.message}`)
        activeAlerts.value = activeAlerts.value.filter(a => a.id !== selectedAlert.value.id)
        alertDialogVisible.value = false
      } catch (error) {
        ElMessage.error('确认告警失败，请稍后再试')
      }
    }
    
    const exportAlerts = () => {
      ElMessage.success('告警数据导出功能开发中')
    }
    
    const handleAlertsPageChange = (page) => {
      alertsPage.value = page
      // 在实际应用中，这里应该重新获取告警列表
    }
    
    const handleAlertsPageSizeChange = (size) => {
      alertsPageSize.value = size
      // 在实际应用中，这里应该重新获取告警列表
    }
    
    // 初始化图表
    const initCharts = () => {
      // 猪群分布图
      if (pigDistributionChart.value) {
        pigChart = echarts.init(pigDistributionChart.value)
        updatePigChart()
        
        // 响应窗口大小变化
        window.addEventListener('resize', () => {
          pigChart.resize()
        })
      }
      
      // 饲料消耗趋势图
      if (feedConsumptionChart.value) {
        feedChart = echarts.init(feedConsumptionChart.value)
        updateFeedChart()
        
        // 响应窗口大小变化
        window.addEventListener('resize', () => {
          feedChart.resize()
        })
      }
    }
    
    // 更新猪群分布图
    const updatePigChart = () => {
      if (!pigChart) return
      
      let option = {}
      
      if (pigDataType.value === 'weight') {
        option = {
          title: {
            text: '猪群体重分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 10,
            data: ['<50kg', '50-80kg', '80-100kg', '100-120kg', '>120kg']
          },
          series: [
            {
              name: '体重分布',
              type: 'pie',
              radius: ['40%', '70%'],
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
                { value: 150, name: '<50kg' },
                { value: 320, name: '50-80kg' },
                { value: 480, name: '80-100kg' },
                { value: 250, name: '100-120kg' },
                { value: 56, name: '>120kg' }
              ]
            }
          ]
        }
      } else if (pigDataType.value === 'age') {
        option = {
          title: {
            text: '猪群年龄分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: ['<1月', '1-2月', '2-3月', '3-4月', '4-5月', '5-6月', '>6月']
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '数量',
              type: 'bar',
              data: [120, 200, 280, 350, 190, 80, 36],
              itemStyle: {
                color: function(params) {
                  const colorList = ['#91cc75', '#5470c6', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4']
                  return colorList[params.dataIndex]
                }
              }
            }
          ]
        }
      } else if (pigDataType.value === 'health') {
        option = {
          title: {
            text: '猪群健康状态',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 10,
            data: ['健康', '需观察', '生病', '治疗中', '隔离']
          },
          series: [
            {
              name: '健康状态',
              type: 'pie',
              radius: '70%',
              center: ['50%', '50%'],
              data: [
                { value: 1150, name: '健康', itemStyle: { color: '#67C23A' } },
                { value: 65, name: '需观察', itemStyle: { color: '#E6A23C' } },
                { value: 15, name: '生病', itemStyle: { color: '#F56C6C' } },
                { value: 18, name: '治疗中', itemStyle: { color: '#409EFF' } },
                { value: 8, name: '隔离', itemStyle: { color: '#909399' } }
              ],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        }
      }
      
      pigChart.setOption(option)
    }
    
    // 更新饲料消耗趋势图
    const updateFeedChart = () => {
      if (!feedChart) return
      
      let xAxisData = []
      let seriesData = []
      
      if (feedTimeRange.value === 'week') {
        xAxisData = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        seriesData = [
          { name: '标准饲料A', data: [120, 132, 125, 128, 130, 115, 122] },
          { name: '生长促进饲料B', data: [80, 85, 82, 78, 83, 75, 80] },
          { name: '营养强化饲料C', data: [40, 38, 42, 45, 40, 35, 38] }
        ]
      } else if (feedTimeRange.value === 'month') {
        xAxisData = Array.from({ length: 30 }, (_, i) => `${i + 1}日`)
        seriesData = [
          {
            name: '标准饲料A',
            data: Array.from({ length: 30 }, () => Math.floor(Math.random() * 30 + 110))
          },
          {
            name: '生长促进饲料B',
            data: Array.from({ length: 30 }, () => Math.floor(Math.random() * 20 + 70))
          },
          {
            name: '营养强化饲料C',
            data: Array.from({ length: 30 }, () => Math.floor(Math.random() * 15 + 30))
          }
        ]
      } else if (feedTimeRange.value === 'quarter') {
        xAxisData = ['1月', '2月', '3月']
        seriesData = [
          { name: '标准饲料A', data: [3600, 3800, 3750] },
          { name: '生长促进饲料B', data: [2400, 2500, 2450] },
          { name: '营养强化饲料C', data: [1200, 1150, 1250] }
        ]
      }
      
      const option = {
        title: {
          text: '饲料消耗趋势',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        legend: {
          data: ['标准饲料A', '生长促进饲料B', '营养强化饲料C'],
          top: 30
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
          data: xAxisData
        },
        yAxis: {
          type: 'value',
          name: '消耗量 (kg)'
        },
        series: seriesData.map(item => ({
          name: item.name,
          type: 'line',
          stack: 'Total',
          areaStyle: {},
          emphasis: {
            focus: 'series'
          },
          data: item.data
        }))
      }
      
      feedChart.setOption(option)
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
      
      // 设置定时刷新
      const refreshInterval = setInterval(() => {
        refreshData()
      }, 300000) // 每5分钟刷新一次
      
      // 组件卸载时清除定时器
      onBeforeUnmount(() => {
        clearInterval(refreshInterval)
      })
    })
    
    return {
      // 状态
      isCollapse,
      activeMenu,
      userName,
      userAvatar,
      userInitials,
      isAdmin,
      isRefreshing,
      lastUpdatedTime,
      pigDistributionChart,
      feedConsumptionChart,
      pigDataType,
      feedTimeRange,
      monitoringAreas,
      pigStatus,
      feedStocks,
      cameraStreams,
      activeAlerts,
      historyAlerts,
      alertsTab,
      alertsLoading,
      alertsPage,
      alertsPageSize,
      totalActiveAlerts,
      totalHistoryAlerts,
      activeAlertsCount,
      alertDialogVisible,
      selectedAlert,
      
      // 方法
      toggleSidebar,
      handleCommand,
      refreshData,
      getAreaStatusType,
      getParamColor,
      getParamClass,
      viewAreaDetails,
      viewAreaHistory,
      updatePigChart,
      updateFeedChart,
      viewPigDetails,
      exportPigData,
      getFeedStockClass,
      getFeedStockStatus,
      orderFeed,
      viewFullscreen,
      viewRecordings,
      cameraSettings,
      getAlertTypeTag,
      getAlertLevelTag,
      showAlerts,
      acknowledgeAlert,
      acknowledgeAllAlerts,
      viewAlertDetails,
      acknowledgeAlertFromDialog,
      exportAlerts,
      handleAlertsPageChange,
      handleAlertsPageSizeChange
    }
  }
}
</script>

<style scoped>
.monitoring-page {
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

.monitoring-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.monitoring-header h1 {
  margin: 0;
  font-size: 1.8rem;
  color: #333;
}

.monitoring-actions {
  display: flex;
  align-items: center;
}

.last-updated {
  margin-right: 15px;
  color: #666;
  font-size: 0.9rem;
}

/* 监控区域样式 */
.monitoring-section {
  margin-bottom: 30px;
}

.section-title {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 20px;
}

.section-title .el-icon {
  margin-right: 10px;
}

/* 环境卡片样式 */
.env-card {
  height: 100%;
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.env-card:hover {
  transform: translateY(-5px);
}

.env-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.env-card-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.env-card-body {
  padding: 15px;
}

.env-param {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.env-param:last-child {
  margin-bottom: 0;
}

.param-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  border-radius: 50%;
  margin-right: 15px;
}

.param-info {
  flex: 1;
}

.param-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 5px;
}

.param-value {
  font-size: 1.2rem;
  font-weight: bold;
}

.param-normal {
  color: #67C23A;
}

.param-warning {
  color: #E6A23C;
}

.param-danger {
  color: #F56C6C;
}

.param-trend {
  margin-left: 10px;
}

.env-card-footer {
  display: flex;
  justify-content: space-between;
  padding: 10px 15px;
  border-top: 1px solid #eee;
}

/* 猪群状态卡片样式 */
.chart-card {
  height: 100%;
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

.pig-status-card {
  height: 100%;
  margin-bottom: 20px;
}

.pig-status-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  padding: 15px;
}

.status-item {
  display: flex;
  flex-direction: column;
}

.status-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 5px;
}

.status-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.status-trend {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
}

.status-trend.up {
  color: #67C23A;
}

.status-trend.down {
  color: #F56C6C;
}

.pig-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  padding: 10px 15px;
}

/* 饲料状态卡片样式 */
.feed-status-card {
  height: 100%;
  margin-bottom: 20px;
}

.feed-status-content {
  padding: 15px;
}

.feed-item {
  margin-bottom: 20px;
}

.feed-item:last-child {
  margin-bottom: 0;
}

.feed-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.feed-name {
  font-weight: bold;
  color: #333;
}

.feed-stock-info {
  font-size: 0.9rem;
}

.stock-normal {
  color: #67C23A;
}

.stock-warning {
  color: #E6A23C;
}

.stock-danger {
  color: #F56C6C;
}

.feed-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.feed-estimate {
  font-size: 0.9rem;
  color: #666;
}

/* 摄像头卡片样式 */
.camera-card {
  height: 100%;
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.camera-card:hover {
  transform: translateY(-5px);
}

.camera-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.camera-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.camera-stream {
  height: 180px;
  overflow: hidden;
  position: relative;
}

.camera-stream img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.camera-offline {
  height: 180px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
  color: #909399;
}

.camera-offline p {
  margin-top: 10px;
}

.camera-actions {
  padding: 10px 15px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: center;
}

/* 告警卡片样式 */
.alerts-card {
  margin-bottom: 20px;
}

.alert-tabs {
  display: flex;
  align-items: center;
}

.alert-actions {
  display: flex;
  gap: 10px;
}

.alert-badge {
  margin-left: 10px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

/* 告警详情对话框样式 */
.alert-detail {
  max-height: 500px;
  overflow-y: auto;
}

.alert-detail-item {
  margin-bottom: 15px;
  display: flex;
}

.detail-label {
  width: 100px;
  font-weight: bold;
  color: #333;
}

.detail-value {
  flex: 1;
}

.parameters-list {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.parameter-item {
  display: flex;
}

.parameter-name {
  width: 120px;
  color: #666;
}

.parameter-value {
  flex: 1;
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
  
  .monitoring-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .monitoring-actions {
    margin-top: 10px;
  }
  
  .pig-status-content {
    grid-template-columns: 1fr;
  }
  
  .camera-stream,
  .camera-offline {
    height: 150px;
  }
  
  .alert-detail-item {
    flex-direction: column;
  }
  
  .detail-label {
    width: 100%;
    margin-bottom: 5px;
  }
}

@media (max-width: 576px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .alert-actions {
    margin-top: 10px;
  }
  
  .chart-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .chart-header h3 {
    margin-bottom: 10px;
  }
}
</style>
