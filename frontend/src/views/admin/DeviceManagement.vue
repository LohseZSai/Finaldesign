<template>
  <div class="device-management-page">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="250px" class="sidebar">
        <div class="logo-container">
          <img src="@/assets/logo.svg" alt="泓泰生物科技" class="logo" />
          <h2>智能养殖管理系统</h2>
        </div>
        
        <el-menu
          default-active="/admin/devices"
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
              <el-breadcrumb-item :to="{ path: '/admin' }">管理控制台</el-breadcrumb-item>
              <el-breadcrumb-item>设备管理</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          
          <div class="header-right">
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
          <div class="page-header">
            <h1>设备管理</h1>
            <el-button type="primary" @click="showAddDeviceDialog">
              <el-icon><Plus /></el-icon> 添加设备
            </el-button>
          </div>
          
          <!-- 设备概览 -->
          <el-row :gutter="20" class="device-overview">
            <el-col :xs="24" :sm="12" :md="6">
              <el-card shadow="hover" class="overview-card">
                <div class="overview-content">
                  <div class="overview-icon">
                    <el-icon><Monitor /></el-icon>
                  </div>
                  <div class="overview-data">
                    <div class="overview-value">{{ deviceStats.total }}</div>
                    <div class="overview-label">设备总数</div>
                  </div>
                </div>
              </el-card>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="6">
              <el-card shadow="hover" class="overview-card">
                <div class="overview-content">
                  <div class="overview-icon online">
                    <el-icon><CircleCheck /></el-icon>
                  </div>
                  <div class="overview-data">
                    <div class="overview-value">{{ deviceStats.online }}</div>
                    <div class="overview-label">在线设备</div>
                  </div>
                </div>
              </el-card>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="6">
              <el-card shadow="hover" class="overview-card">
                <div class="overview-content">
                  <div class="overview-icon offline">
                    <el-icon><CircleClose /></el-icon>
                  </div>
                  <div class="overview-data">
                    <div class="overview-value">{{ deviceStats.offline }}</div>
                    <div class="overview-label">离线设备</div>
                  </div>
                </div>
              </el-card>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="6">
              <el-card shadow="hover" class="overview-card">
                <div class="overview-content">
                  <div class="overview-icon warning">
                    <el-icon><Warning /></el-icon>
                  </div>
                  <div class="overview-data">
                    <div class="overview-value">{{ deviceStats.warning }}</div>
                    <div class="overview-label">告警设备</div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
          
          <!-- 搜索和筛选 -->
          <div class="filter-container">
            <el-input
              v-model="searchQuery"
              placeholder="搜索设备名称/ID"
              class="search-input"
              clearable
              @clear="handleSearch"
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            
            <el-select v-model="filterType" placeholder="设备类型" clearable @change="handleSearch">
              <el-option label="全部类型" value="" />
              <el-option label="环境传感器" value="sensor" />
              <el-option label="控制设备" value="controller" />
              <el-option label="摄像头" value="camera" />
              <el-option label="饲喂设备" value="feeder" />
            </el-select>
            
            <el-select v-model="filterStatus" placeholder="设备状态" clearable @change="handleSearch">
              <el-option label="全部状态" value="" />
              <el-option label="在线" value="online" />
              <el-option label="离线" value="offline" />
              <el-option label="告警" value="warning" />
            </el-select>
            
            <el-select v-model="filterLocation" placeholder="设备位置" clearable @change="handleSearch">
              <el-option label="全部位置" value="" />
              <el-option v-for="location in locations" :key="location" :label="location" :value="location" />
            </el-select>
          </div>
          
          <!-- 设备列表 -->
          <el-table
            :data="filteredDevices"
            style="width: 100%"
            v-loading="loading"
            border
            stripe
          >
            <el-table-column prop="id" label="设备ID" width="120" />
            <el-table-column prop="name" label="设备名称" min-width="150" />
            <el-table-column prop="type" label="设备类型" width="120">
              <template #default="scope">
                <el-tag :type="getDeviceTypeTag(scope.row.type)">
                  {{ getDeviceTypeName(scope.row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="location" label="安装位置" width="120" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getStatusTagType(scope.row.status)">
                  {{ getStatusName(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="lastActive" label="最后活跃时间" width="180" />
            <el-table-column label="操作" width="250" fixed="right">
              <template #default="scope">
                <el-button
                  type="primary"
                  size="small"
                  @click="handleDetail(scope.row)"
                >
                  详情
                </el-button>
                <el-button
                  type="success"
                  size="small"
                  @click="handleControl(scope.row)"
                  :disabled="scope.row.status === 'offline'"
                >
                  控制
                </el-button>
                <el-button
                  type="danger"
                  size="small"
                  @click="handleDelete(scope.row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <!-- 分页 -->
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              :total="totalDevices"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </el-main>
      </el-container>
    </el-container>
    
    <!-- 添加设备对话框 -->
    <el-dialog
      v-model="addDialogVisible"
      title="添加设备"
      width="600px"
      destroy-on-close
    >
      <el-form
        :model="deviceForm"
        :rules="deviceRules"
        ref="deviceFormRef"
        label-width="100px"
        label-position="right"
      >
        <el-form-item label="设备名称" prop="name">
          <el-input v-model="deviceForm.name" placeholder="请输入设备名称" />
        </el-form-item>
        
        <el-form-item label="设备类型" prop="type">
          <el-select v-model="deviceForm.type" placeholder="请选择设备类型">
            <el-option label="环境传感器" value="sensor" />
            <el-option label="控制设备" value="controller" />
            <el-option label="摄像头" value="camera" />
            <el-option label="饲喂设备" value="feeder" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="安装位置" prop="location">
          <el-select v-model="deviceForm.location" placeholder="请选择安装位置">
            <el-option v-for="location in locations" :key="location" :label="location" :value="location" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="设备IP" prop="ip">
          <el-input v-model="deviceForm.ip" placeholder="请输入设备IP地址" />
        </el-form-item>
        
        <el-form-item label="MAC地址" prop="mac">
          <el-input v-model="deviceForm.mac" placeholder="请输入设备MAC地址" />
        </el-form-item>
        
        <el-form-item label="备注" prop="notes">
          <el-input
            v-model="deviceForm.notes"
            type="textarea"
            rows="3"
            placeholder="请输入设备备注信息"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="addDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitDeviceForm" :loading="submitting">
            添加
          </el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 设备详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="设备详情"
      width="700px"
    >
      <div v-if="currentDevice" class="device-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="设备ID">{{ currentDevice.id }}</el-descriptions-item>
          <el-descriptions-item label="设备名称">{{ currentDevice.name }}</el-descriptions-item>
          <el-descriptions-item label="设备类型">
            <el-tag :type="getDeviceTypeTag(currentDevice.type)">
              {{ getDeviceTypeName(currentDevice.type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="设备状态">
            <el-tag :type="getStatusTagType(currentDevice.status)">
              {{ getStatusName(currentDevice.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="安装位置">{{ currentDevice.location }}</el-descriptions-item>
          <el-descriptions-item label="最后活跃时间">{{ currentDevice.lastActive }}</el-descriptions-item>
          <el-descriptions-item label="设备IP">{{ currentDevice.ip }}</el-descriptions-item>
          <el-descriptions-item label="MAC地址">{{ currentDevice.mac }}</el-descriptions-item>
          <el-descriptions-item label="安装日期">{{ currentDevice.installDate }}</el-descriptions-item>
          <el-descriptions-item label="固件版本">{{ currentDevice.firmwareVersion }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ currentDevice.notes }}</el-descriptions-item>
        </el-descriptions>
        
        <div class="detail-section">
          <h3>设备数据</h3>
          <div v-if="currentDevice.type === 'sensor'" class="sensor-data">
            <el-row :gutter="20">
              <el-col :span="8" v-for="(value, key) in currentDevice.data" :key="key">
                <el-card shadow="hover" class="data-card">
                  <div class="data-value">{{ value.value }}{{ value.unit }}</div>
                  <div class="data-label">{{ value.label }}</div>
                </el-card>
              </el-col>
            </el-row>
          </div>
          
          <div v-else-if="currentDevice.type === 'camera'" class="camera-data">
            <el-card shadow="hover" class="camera-card">
              <div class="camera-stream">
                <img :src="currentDevice.streamUrl" alt="摄像头画面" />
              </div>
              <div class="camera-controls">
                <el-button-group>
                  <el-button type="primary" :icon="VideoPlay">开始</el-button>
                  <el-button type="warning" :icon="VideoPause">暂停</el-button>
                  <el-button type="info" :icon="Camera">截图</el-button>
                </el-button-group>
              </div>
            </el-card>
          </div>
          
          <div v-else class="other-data">
            <el-empty description="暂无数据" />
          </div>
        </div>
        
        <div class="detail-section">
          <h3>历史记录</h3>
          <el-tabs>
            <el-tab-pane label="告警记录">
              <el-table :data="deviceAlerts" style="width: 100%">
                <el-table-column prop="time" label="时间" width="180" />
                <el-table-column prop="type" label="告警类型" width="120">
                  <template #default="scope">
                    <el-tag type="danger">{{ scope.row.type }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="message" label="告警内容" />
                <el-table-column prop="status" label="状态" width="100">
                  <template #default="scope">
                    <el-tag :type="scope.row.status === 'resolved' ? 'success' : 'warning'">
                      {{ scope.row.status === 'resolved' ? '已解决' : '未解决' }}
                    </el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="维护记录">
              <el-table :data="deviceMaintenance" style="width: 100%">
                <el-table-column prop="time" label="时间" width="180" />
                <el-table-column prop="type" label="维护类型" width="120" />
                <el-table-column prop="operator" label="操作人" width="120" />
                <el-table-column prop="description" label="维护内容" />
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>
    </el-dialog>
    
    <!-- 设备控制对话框 -->
    <el-dialog
      v-model="controlDialogVisible"
      title="设备控制"
      width="600px"
    >
      <div v-if="currentDevice" class="device-control">
        <div class="control-header">
          <h3>{{ currentDevice.name }}</h3>
          <el-tag :type="getStatusTagType(currentDevice.status)">
            {{ getStatusName(currentDevice.status) }}
          </el-tag>
        </div>
        
        <div v-if="currentDevice.type === 'controller'" class="controller-controls">
          <el-card shadow="hover" class="control-card">
            <template #header>
              <div class="control-card-header">
                <span>环境控制</span>
              </div>
            </template>
            <el-form label-position="left" label-width="100px">
              <el-form-item label="设备开关">
                <el-switch
                  v-model="controlForm.power"
                  active-text="开启"
                  inactive-text="关闭"
                  @change="handlePowerChange"
                />
              </el-form-item>
              <el-form-item label="运行模式">
                <el-radio-group v-model="controlForm.mode" @change="handleModeChange">
                  <el-radio label="auto">自动模式</el-radio>
                  <el-radio label="manual">手动模式</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="温度设定">
                <el-slider
                  v-model="controlForm.temperature"
                  :min="16"
                  :max="30"
                  :step="0.5"
                  :disabled="controlForm.mode === 'auto'"
                  show-input
                  @change="handleTemperatureChange"
                />
              </el-form-item>
              <el-form-item label="湿度设定">
                <el-slider
                  v-model="controlForm.humidity"
                  :min="40"
                  :max="80"
                  :step="1"
                  :disabled="controlForm.mode === 'auto'"
                  show-input
                  @change="handleHumidityChange"
                />
              </el-form-item>
            </el-form>
          </el-card>
        </div>
        
        <div v-else-if="currentDevice.type === 'feeder'" class="feeder-controls">
          <el-card shadow="hover" class="control-card">
            <template #header>
              <div class="control-card-header">
                <span>饲喂控制</span>
              </div>
            </template>
            <el-form label-position="left" label-width="100px">
              <el-form-item label="设备开关">
                <el-switch
                  v-model="controlForm.power"
                  active-text="开启"
                  inactive-text="关闭"
                  @change="handlePowerChange"
                />
              </el-form-item>
              <el-form-item label="饲喂模式">
                <el-radio-group v-model="controlForm.feedMode" @change="handleFeedModeChange">
                  <el-radio label="auto">自动饲喂</el-radio>
                  <el-radio label="manual">手动饲喂</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="饲喂量">
                <el-input-number
                  v-model="controlForm.feedAmount"
                  :min="1"
                  :max="100"
                  :step="1"
                  :disabled="controlForm.feedMode === 'auto'"
                  @change="handleFeedAmountChange"
                />
                <span class="unit">kg</span>
              </el-form-item>
              <el-form-item v-if="controlForm.feedMode === 'manual'">
                <el-button type="primary" @click="handleManualFeed">立即饲喂</el-button>
              </el-form-item>
              <el-form-item label="饲喂计划" v-if="controlForm.feedMode === 'auto'">
                <el-table :data="feedSchedule" style="width: 100%">
                  <el-table-column prop="time" label="时间" width="120" />
                  <el-table-column prop="amount" label="饲喂量(kg)" width="100" />
                  <el-table-column label="操作" width="80">
                    <template #default="scope">
                      <el-button
                        type="danger"
                        size="small"
                        circle
                        @click="removeFeedSchedule(scope.$index)"
                      >
                        <el-icon><Delete /></el-icon>
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
                <div class="add-schedule">
                  <el-time-picker
                    v-model="newScheduleTime"
                    format="HH:mm"
                    placeholder="选择时间"
                    style="width: 120px;"
                  />
                  <el-input-number
                    v-model="newScheduleAmount"
                    :min="1"
                    :max="100"
                    :step="1"
                    style="width: 100px; margin: 0 10px;"
                  />
                  <el-button type="primary" @click="addFeedSchedule">添加</el-button>
                </div>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
        
        <div v-else>
          <el-empty description="该设备类型不支持控制操作" />
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  HomeFilled,
  Monitor,
  DataLine,
  Connection,
  User,
  Setting,
  Search,
  Plus,
  ArrowDown,
  CircleCheck,
  CircleClose,
  Warning,
  Delete,
  VideoPlay,
  VideoPause,
  Camera
} from '@element-plus/icons-vue'

export default {
  name: 'DeviceManagementPage',
  components: {
    HomeFilled,
    Monitor,
    DataLine,
    Connection,
    User,
    Setting,
    Search,
    Plus,
    ArrowDown,
    CircleCheck,
    CircleClose,
    Warning,
    Delete,
    VideoPlay,
    VideoPause,
    Camera
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    // 侧边栏状态
    const isCollapse = ref(false)
    
    // 用户信息
    const userName = computed(() => authStore.user?.name || '用户')
    const userAvatar = computed(() => authStore.user?.avatar || '')
    const userInitials = computed(() => {
      const name = authStore.user?.name || ''
      return name.substring(0, 1).toUpperCase()
    })
    const isAdmin = computed(() => authStore.isAdmin)
    
    // 设备统计
    const deviceStats = reactive({
      total: 0,
      online: 0,
      offline: 0,
      warning: 0
    })
    
    // 设备列表状态
    const loading = ref(false)
    const devices = ref([])
    const totalDevices = ref(0)
    const currentPage = ref(1)
    const pageSize = ref(10)
    
    // 搜索和筛选
    const searchQuery = ref('')
    const filterType = ref('')
    const filterStatus = ref('')
    const filterLocation = ref('')
    
    // 位置列表
    const locations = ref([
      '1号猪舍',
      '2号猪舍',
      '3号猪舍',
      '饲料仓库',
      '中控室'
    ])
    
    // 对话框状态
    const addDialogVisible = ref(false)
    const detailDialogVisible = ref(false)
    const controlDialogVisible = ref(false)
    const submitting = ref(false)
    const deviceFormRef = ref(null)
    
    // 当前选中的设备
    const currentDevice = ref(null)
    
    // 设备表单
    const deviceForm = reactive({
      name: '',
      type: '',
      location: '',
      ip: '',
      mac: '',
      notes: ''
    })
    
    // 控制表单
    const controlForm = reactive({
      power: true,
      mode: 'auto',
      temperature: 24,
      humidity: 60,
      feedMode: 'auto',
      feedAmount: 10
    })
    
    // 饲喂计划
    const feedSchedule = ref([
      { time: '08:00', amount: 20 },
      { time: '16:00', amount: 15 }
    ])
    const newScheduleTime = ref('')
    const newScheduleAmount = ref(10)
    
    // 设备告警记录
    const deviceAlerts = ref([
      {
        time: '2025-03-15 08:23',
        type: '温度异常',
        message: '设备检测到温度过高 (32.5°C)',
        status: 'resolved'
      },
      {
        time: '2025-03-14 23:45',
        type: '连接中断',
        message: '设备连接中断超过30分钟',
        status: 'active'
      }
    ])
    
    // 设备维护记录
    const deviceMaintenance = ref([
      {
        time: '2025-03-10 14:30',
        type: '例行检查',
        operator: '张三',
        description: '设备例行检查，清理灰尘，检查连接'
      },
      {
        time: '2025-02-20 09:15',
        type: '固件升级',
        operator: '李四',
        description: '升级设备固件至v2.3.5版本'
      }
    ])
    
    // 表单验证规则
    const deviceRules = {
      name: [
        { required: true, message: '请输入设备名称', trigger: 'blur' },
        { min: 2, max: 30, message: '长度在 2 到 30 个字符', trigger: 'blur' }
      ],
      type: [
        { required: true, message: '请选择设备类型', trigger: 'change' }
      ],
      location: [
        { required: true, message: '请选择安装位置', trigger: 'change' }
      ],
      ip: [
        { required: true, message: '请输入设备IP地址', trigger: 'blur' }
      ],
      mac: [
        { required: true, message: '请输入设备MAC地址', trigger: 'blur' }
      ]
    }
    
    // 设备管理方法
    const handleCommand = () => {
      // 实现命令处理逻辑
    }
    
    const toggleSidebar = () => {
      // 实现侧边栏切换逻辑
    }
    
    const showAddDeviceDialog = () => {
      // 实现显示添加设备对话框逻辑
    }
    
    const handleSearch = () => {
      // 实现搜索逻辑
    }
    
    const handleSizeChange = () => {
      // 实现分页大小改变逻辑
    }
    
    const handleCurrentChange = () => {
      // 实现当前页改变逻辑
    }
    
    const handleDetail = (device) => {
      // 实现查看设备详情逻辑
    }
    
    const handleControl = (device) => {
      // 实现控制设备逻辑
    }
    
    const handleDelete = (device) => {
      // 实现删除设备逻辑
    }
    
    const handlePowerChange = () => {
      // 实现设备开关改变逻辑
    }
    
    const handleModeChange = () => {
      // 实现设备运行模式改变逻辑
    }
    
    const handleTemperatureChange = () => {
      // 实现温度设定改变逻辑
    }
    
    const handleHumidityChange = () => {
      // 实现湿度设定改变逻辑
    }
    
    const handleFeedModeChange = () => {
      // 实现饲喂模式改变逻辑
    }
    
    const handleFeedAmountChange = () => {
      // 实现饲喂量改变逻辑
    }
    
    const handleManualFeed = () => {
      // 实现手动饲喂逻辑
    }
    
    const removeFeedSchedule = (index) => {
      // 实现移除饲喂计划逻辑
    }
    
    const addFeedSchedule = () => {
      // 实现添加饲喂计划逻辑
    }
    
    return {
      // 用户信息
      userName,
      userAvatar,
      userInitials,
      isAdmin,
      
      // 侧边栏状态
      isCollapse,
      toggleSidebar,
      
      // 设备统计
      deviceStats,
      
      // 设备列表状态
      loading,
      devices,
      totalDevices,
      currentPage,
      pageSize,
      
      // 搜索和筛选
      searchQuery,
      filterType,
      filterStatus,
      filterLocation,
      locations,
      handleSearch,
      handleSizeChange,
      handleCurrentChange,
      
      // 设备操作
      handleDetail,
      handleControl,
      handleDelete,
      handleCommand,
      
      // 设备表单
      addDialogVisible,
      showAddDeviceDialog,
      deviceForm,
      deviceRules,
      deviceFormRef,
      submitting,
      submitDeviceForm,
      
      // 设备详情
      detailDialogVisible,
      currentDevice,
      deviceAlerts,
      deviceMaintenance,
      
      // 设备控制
      controlDialogVisible,
      controlForm,
      handlePowerChange,
      handleModeChange,
      handleTemperatureChange,
      handleHumidityChange,
      handleFeedModeChange,
      handleFeedAmountChange,
      handleManualFeed,
      
      // 饲喂计划
      feedSchedule,
      newScheduleTime,
      newScheduleAmount,
      addFeedSchedule,
      removeFeedSchedule,
      
      // 辅助函数
      getDeviceTypeTag: (type) => {
        const typeMap = {
          sensor: 'info',
          controller: 'success',
          camera: 'warning',
          feeder: 'primary'
        }
        return typeMap[type] || 'info'
      },
      getDeviceTypeName: (type) => {
        const typeMap = {
          sensor: '环境传感器',
          controller: '控制设备',
          camera: '摄像头',
          feeder: '饲喂设备'
        }
        return typeMap[type] || '未知设备'
      },
      getStatusTagType: (status) => {
        const statusMap = {
          online: 'success',
          offline: 'info',
          warning: 'warning',
          error: 'danger'
        }
        return statusMap[status] || 'info'
      },
      getStatusName: (status) => {
        const statusMap = {
          online: '在线',
          offline: '离线',
          warning: '告警',
          error: '错误'
        }
        return statusMap[status] || '未知状态'
      },
      
      // 计算属性
      filteredDevices: computed(() => {
        // 这里应该实现根据搜索条件过滤设备的逻辑
        // 简单示例：
        return devices.value.filter(device => {
          const matchQuery = !searchQuery.value || 
            device.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            device.id.toLowerCase().includes(searchQuery.value.toLowerCase())
          const matchType = !filterType.value || device.type === filterType.value
          const matchStatus = !filterStatus.value || device.status === filterStatus.value
          const matchLocation = !filterLocation.value || device.location === filterLocation.value
          
          return matchQuery && matchType && matchStatus && matchLocation
        })
      })
    }
  }
}
</script>

<style scoped>
.device-management-page {
  height: 100%;
}

/* 侧边栏样式 */
.sidebar {
  background-color: #001529;
  color: #fff;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
  transition: width 0.3s;
  overflow-y: auto;
}

.logo-container {
  padding: 16px;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  height: 40px;
  margin-bottom: 8px;
}

.logo-container h2 {
  color: #fff;
  font-size: 16px;
  margin: 0;
}

.sidebar-menu {
  border-right: none;
}

/* 头部样式 */
.header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  height: 64px;
}

.header-left {
  display: flex;
  align-items: center;
}

.toggle-button {
  margin-right: 16px;
  font-size: 18px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.username {
  margin: 0 8px;
  color: #333;
}

/* 主内容区样式 */
.main-content {
  padding: 20px;
  background-color: #f0f2f5;
  min-height: calc(100vh - 64px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h1 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

/* 设备概览卡片样式 */
.device-overview {
  margin-bottom: 24px;
}

.overview-card {
  margin-bottom: 16px;
}

.overview-content {
  display: flex;
  align-items: center;
}

.overview-icon {
  font-size: 48px;
  margin-right: 16px;
  color: #409EFF;
}

.overview-icon.online {
  color: #67C23A;
}

.overview-icon.offline {
  color: #909399;
}

.overview-icon.warning {
  color: #E6A23C;
}

.overview-data {
  flex: 1;
}

.overview-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  line-height: 1.2;
}

.overview-label {
  font-size: 14px;
  color: #666;
}

/* 搜索和筛选区域样式 */
.filter-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
}

.search-input {
  width: 300px;
}

/* 分页样式 */
.pagination-container {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
}

/* 设备详情样式 */
.device-detail {
  padding: 16px;
}

.detail-section {
  margin-top: 24px;
}

.detail-section h3 {
  margin-bottom: 16px;
  font-size: 18px;
  color: #333;
}

.sensor-data {
  margin-top: 16px;
}

.data-card {
  text-align: center;
  padding: 16px;
  margin-bottom: 16px;
}

.data-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 8px;
}

.data-label {
  font-size: 14px;
  color: #666;
}

.camera-card {
  margin-top: 16px;
}

.camera-stream {
  width: 100%;
  height: 300px;
  background-color: #000;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.camera-stream img {
  max-width: 100%;
  max-height: 100%;
}

.camera-controls {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

/* 设备控制样式 */
.device-control {
  padding: 16px;
}

.control-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.control-header h3 {
  margin: 0;
  font-size: 18px;
}

.control-card {
  margin-bottom: 16px;
}

.control-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.add-schedule {
  display: flex;
  align-items: center;
  margin-top: 16px;
}

.unit {
  margin-left: 8px;
  color: #666;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .filter-container {
    flex-direction: column;
  }
  
  .search-input {
    width: 100%;
  }
  
  .overview-icon {
    font-size: 36px;
  }
  
  .overview-value {
    font-size: 24px;
  }
}
</style> 