<template>
  <div class="employee-management-page">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="250px" class="sidebar">
        <div class="logo-container">
          <img src="@/assets/logo.svg" alt="泓泰生物科技" class="logo" />
          <h2>智能养殖管理系统</h2>
        </div>
        
        <el-menu
          default-active="/admin/employees"
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
          
          <el-menu-item index="/admin/employees">
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
              <el-breadcrumb-item>员工管理</el-breadcrumb-item>
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
            <h1>员工管理</h1>
            <el-button type="primary" @click="showAddEmployeeDialog">
              <el-icon><Plus /></el-icon> 添加员工
            </el-button>
          </div>
          
          <!-- 搜索和筛选 -->
          <div class="filter-container">
            <el-input
              v-model="searchQuery"
              placeholder="搜索员工姓名/工号"
              class="search-input"
              clearable
              @clear="handleSearch"
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            
            <el-select v-model="filterRole" placeholder="角色筛选" clearable @change="handleSearch">
              <el-option label="全部角色" value="" />
              <el-option label="管理员" value="admin" />
              <el-option label="技术员" value="technician" />
              <el-option label="饲养员" value="breeder" />
            </el-select>
            
            <el-select v-model="filterStatus" placeholder="状态筛选" clearable @change="handleSearch">
              <el-option label="全部状态" value="" />
              <el-option label="在职" value="active" />
              <el-option label="离职" value="inactive" />
            </el-select>
          </div>
          
          <!-- 员工列表 -->
          <el-table
            :data="filteredEmployees"
            style="width: 100%"
            v-loading="loading"
            border
            stripe
          >
            <el-table-column prop="id" label="工号" width="80" />
            <el-table-column label="员工信息" min-width="200">
              <template #default="scope">
                <div class="employee-info">
                  <el-avatar :size="40" :src="scope.row.avatar">
                    {{ getInitials(scope.row.name) }}
                  </el-avatar>
                  <div class="employee-details">
                    <div class="employee-name">{{ scope.row.name }}</div>
                    <div class="employee-email">{{ scope.row.email }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="phone" label="联系电话" width="130" />
            <el-table-column prop="department" label="部门" width="120" />
            <el-table-column prop="role" label="角色" width="100">
              <template #default="scope">
                <el-tag :type="getRoleTagType(scope.row.role)">
                  {{ getRoleName(scope.row.role) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="80">
              <template #default="scope">
                <el-tag :type="scope.row.status === 'active' ? 'success' : 'info'">
                  {{ scope.row.status === 'active' ? '在职' : '离职' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="joinDate" label="入职日期" width="120" />
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="scope">
                <el-button
                  type="primary"
                  size="small"
                  @click="handleEdit(scope.row)"
                  :disabled="!isAdmin"
                >
                  编辑
                </el-button>
                <el-button
                  type="danger"
                  size="small"
                  @click="handleDelete(scope.row)"
                  :disabled="!isAdmin"
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
              :total="totalEmployees"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </el-main>
      </el-container>
    </el-container>
    
    <!-- 添加/编辑员工对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑员工' : '添加员工'"
      width="600px"
      destroy-on-close
    >
      <el-form
        :model="employeeForm"
        :rules="employeeRules"
        ref="employeeFormRef"
        label-width="100px"
        label-position="right"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="employeeForm.name" placeholder="请输入员工姓名" />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="employeeForm.email" placeholder="请输入员工邮箱" />
        </el-form-item>
        
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="employeeForm.phone" placeholder="请输入联系电话" />
        </el-form-item>
        
        <el-form-item label="部门" prop="department">
          <el-select v-model="employeeForm.department" placeholder="请选择部门">
            <el-option label="生产部" value="production" />
            <el-option label="技术部" value="technology" />
            <el-option label="管理部" value="management" />
            <el-option label="后勤部" value="logistics" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="角色" prop="role">
          <el-select v-model="employeeForm.role" placeholder="请选择角色">
            <el-option label="管理员" value="admin" />
            <el-option label="技术员" value="technician" />
            <el-option label="饲养员" value="breeder" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="employeeForm.status">
            <el-radio label="active">在职</el-radio>
            <el-radio label="inactive">离职</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="入职日期" prop="joinDate">
          <el-date-picker
            v-model="employeeForm.joinDate"
            type="date"
            placeholder="选择入职日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password" v-if="!isEdit">
          <el-input
            v-model="employeeForm.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword" v-if="!isEdit">
          <el-input
            v-model="employeeForm.confirmPassword"
            type="password"
            placeholder="请确认密码"
            show-password
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitEmployeeForm" :loading="submitting">
            {{ isEdit ? '保存修改' : '添加员工' }}
          </el-button>
        </div>
      </template>
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
  ArrowDown
} from '@element-plus/icons-vue'

export default {
  name: 'EmployeeManagementPage',
  components: {
    HomeFilled,
    Monitor,
    DataLine,
    Connection,
    User,
    Setting,
    Search,
    Plus,
    ArrowDown
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
    
    // 员工列表状态
    const loading = ref(false)
    const employees = ref([])
    const totalEmployees = ref(0)
    const currentPage = ref(1)
    const pageSize = ref(10)
    
    // 搜索和筛选
    const searchQuery = ref('')
    const filterRole = ref('')
    const filterStatus = ref('')
    
    // 对话框状态
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const submitting = ref(false)
    const employeeFormRef = ref(null)
    
    // 员工表单
    const employeeForm = reactive({
      id: '',
      name: '',
      email: '',
      phone: '',
      department: '',
      role: '',
      status: 'active',
      joinDate: '',
      password: '',
      confirmPassword: ''
    })
    
    // 表单验证规则
    const employeeRules = {
      name: [
        { required: true, message: '请输入员工姓名', trigger: 'blur' },
        { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱地址', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      phone: [
        { required: true, message: '请输入联系电话', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
      ],
      department: [
        { required: true, message: '请选择部门', trigger: 'change' }
      ],
      role: [
        { required: true, message: '请选择角色', trigger: 'change' }
      ],
      status: [
        { required: true, message: '请选择状态', trigger: 'change' }
      ],
      joinDate: [
        { required: true, message: '请选择入职日期', trigger: 'change' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, message: '请确认密码', trigger: 'blur' },
        {
          validator: (rule, value, callback) => {
            if (value !== employeeForm.password) {
              callback(new Error('两次输入密码不一致'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }
      ]
    }
    
    // 过滤后的员工列表
    const filteredEmployees = computed(() => {
      return employees.value
    })
    
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
    
    const getInitials = (name) => {
      return name ? name.substring(0, 1).toUpperCase() : ''
    }
    
    const getRoleName = (role) => {
      const roleMap = {
        'admin': '管理员',
        'technician': '技术员',
        'breeder': '饲养员'
      }
      return roleMap[role] || role
    }
    
    const getRoleTagType = (role) => {
      const typeMap = {
        'admin': 'danger',
        'technician': 'warning',
        'breeder': 'success'
      }
      return typeMap[role] || ''
    }
    
    const fetchEmployees = async () => {
      loading.value = true
      try {
        // 这里应该是从API获取数据
        // 模拟API请求
        setTimeout(() => {
          employees.value = [
            {
              id: '1001',
              name: '张三',
              email: 'zhangsan@example.com',
              phone: '13800138001',
              department: 'management',
              role: 'admin',
              status: 'active',
              joinDate: '2022-01-15',
              avatar: ''
            },
            {
              id: '1002',
              name: '李四',
              email: 'lisi@example.com',
              phone: '13800138002',
              department: 'technology',
              role: 'technician',
              status: 'active',
              joinDate: '2022-02-20',
              avatar: ''
            },
            {
              id: '1003',
              name: '王五',
              email: 'wangwu@example.com',
              phone: '13800138003',
              department: 'production',
              role: 'breeder',
              status: 'active',
              joinDate: '2022-03-10',
              avatar: ''
            },
            {
              id: '1004',
              name: '赵六',
              email: 'zhaoliu@example.com',
              phone: '13800138004',
              department: 'logistics',
              role: 'breeder',
              status: 'inactive',
              joinDate: '2022-04-05',
              avatar: ''
            }
          ]
          totalEmployees.value = employees.value.length
          loading.value = false
        }, 500)
      } catch (error) {
        console.error('获取员工列表失败:', error)
        ElMessage.error('获取员工列表失败')
        loading.value = false
      }
    }
    
    const handleSearch = () => {
      // 实际应用中应该调用API进行搜索
      // 这里简单模拟前端过滤
      fetchEmployees()
    }
    
    const handleSizeChange = (size) => {
      pageSize.value = size
      fetchEmployees()
    }
    
    const handleCurrentChange = (page) => {
      currentPage.value = page
      fetchEmployees()
    }
    
    const resetEmployeeForm = () => {
      employeeForm.id = ''
      employeeForm.name = ''
      employeeForm.email = ''
      employeeForm.phone = ''
      employeeForm.department = ''
      employeeForm.role = ''
      employeeForm.status = 'active'
      employeeForm.joinDate = ''
      employeeForm.password = ''
      employeeForm.confirmPassword = ''
    }
    
    const showAddEmployeeDialog = () => {
      isEdit.value = false
      resetEmployeeForm()
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      isEdit.value = true
      Object.keys(employeeForm).forEach(key => {
        if (key !== 'password' && key !== 'confirmPassword') {
          employeeForm[key] = row[key]
        }
      })
      dialogVisible.value = true
    }
    
    const handleDelete = (row) => {
      ElMessageBox.confirm(`确定要删除员工 ${row.name} 吗?`, '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 这里应该调用API删除员工
        ElMessage.success('删除成功')
        fetchEmployees()
      }).catch(() => {})
    }
    
    const submitEmployeeForm = () => {
      employeeFormRef.value.validate(async (valid) => {
        if (valid) {
          submitting.value = true
          try {
            // 这里应该调用API保存员工信息
            setTimeout(() => {
              ElMessage.success(isEdit.value ? '员工信息更新成功' : '员工添加成功')
              dialogVisible.value = false
              fetchEmployees()
              submitting.value = false
            }, 500)
          } catch (error) {
            console.error('保存员工信息失败:', error)
            ElMessage.error('保存失败，请重试')
            submitting.value = false
          }
        } else {
          return false
        }
      })
    }
    
    // 生命周期钩子
    onMounted(() => {
      fetchEmployees()
    })
    
    return {
      isCollapse,
      userName,
      userAvatar,
      userInitials,
      isAdmin,
      loading,
      employees,
      filteredEmployees,
      totalEmployees,
      currentPage,
      pageSize,
      searchQuery,
      filterRole,
      filterStatus,
      dialogVisible,
      isEdit,
      submitting,
      employeeForm,
      employeeRules,
      employeeFormRef,
      toggleSidebar,
      handleCommand,
      getInitials,
      getRoleName,
      getRoleTagType,
      handleSearch,
      handleSizeChange,
      handleCurrentChange,
      showAddEmployeeDialog,
      handleEdit,
      handleDelete,
      submitEmployeeForm
    }
  }
}
</script>

<style scoped>
.employee-management-page {
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

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  font-size: 1.8rem;
  color: #333;
}

/* 筛选区域样式 */
.filter-container {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-input {
  width: 300px;
}

/* 员工信息样式 */
.employee-info {
  display: flex;
  align-items: center;
}

.employee-details {
  margin-left: 10px;
}

.employee-name {
  font-weight: bold;
}

.employee-email {
  font-size: 0.9rem;
  color: #666;
}

/* 分页样式 */
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    z-index: 1000;
  }
  
  .filter-container {
    flex-direction: column;
  }
  
  .search-input {
    width: 100%;
  }
}
</style> 