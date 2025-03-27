<template>
  <div class="signup-page">
    <Navbar />
    
    <div class="signup-container">
      <div class="signup-card">
        <div class="signup-header">
          <h2>注册账号</h2>
          <p>加入泓泰生物科技智能养殖管理系统</p>
        </div>
        
        <el-form
          ref="signupFormRef"
          :model="formData"
          :rules="signupRules"
          label-position="top"
          @submit.prevent="handleSignUp"
        >
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="formData.username"
              placeholder="请输入用户名"
              :prefix-icon="User"
            />
          </el-form-item>
          
          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model="formData.email"
              type="email"
              placeholder="请输入邮箱"
              :prefix-icon="Message"
            />
          </el-form-item>
          
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="formData.password"
              type="password"
              placeholder="请输入密码"
              :prefix-icon="Lock"
              show-password
            />
          </el-form-item>
          
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input
              v-model="formData.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              :prefix-icon="Lock"
              show-password
            />
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              native-type="submit"
              :loading="loading"
              class="signup-button"
            >
              注册
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="signup-footer">
          <p>
            已有账号？
            <el-button link @click="goToLogin">立即登录</el-button>
          </p>
          <p>注册即表示同意<a href="/terms">服务条款</a>和<a href="/privacy">隐私政策</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message } from '@element-plus/icons-vue'
import Navbar from '@/components/layout/Navbar.vue'
import api from '@/utils/api'

export default {
  name: 'SignUpPage',
  components: {
    Navbar
  },
  
  setup() {
    const router = useRouter()
    const signupFormRef = ref(null)
    
    const formData = reactive({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      fullName: ''
    })
    
    const loading = ref(false)
    
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (formData.confirmPassword !== '') {
          signupFormRef.value?.validateField('confirmPassword')
        }
        callback()
      }
    }
    
    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== formData.password) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }
    
    const validateEmail = (rule, value, callback) => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (value === '') {
        callback(new Error('请输入邮箱'))
      } else if (!emailRegex.test(value)) {
        callback(new Error('请输入有效的邮箱地址'))
      } else {
        callback()
      }
    }
    
    const signupRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度应为3-20个字符', trigger: 'blur' }
      ],
      email: [
        { required: true, validator: validateEmail, trigger: 'blur' }
      ],
      password: [
        { required: true, validator: validatePass, trigger: 'blur' },
        { min: 6, message: '密码长度至少为6个字符', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, validator: validatePass2, trigger: 'blur' }
      ]
    }
    
    const handleSignUp = async () => {
      if (!signupFormRef.value) return
      
      await signupFormRef.value.validate(async (valid) => {
        if (valid) {
          try {
            loading.value = true
            const response = await api.post('/auth/register', {
              username: formData.username,
              email: formData.email,
              password: formData.password,
              full_name: formData.username
            })
            
            if (response.status === 200) {
              ElMessage.success('注册成功')
              router.push('/login')
            } else {
              ElMessage.error(response.data?.detail || '注册失败')
            }
          } catch (error) {
            console.error('注册错误:', error)
            const errorMessage = error.response?.data?.detail || '注册失败，请稍后再试'
            ElMessage.error(errorMessage)
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    const goToLogin = () => {
      router.push('/login')
    }
    
    return {
      signupFormRef,
      formData,
      signupRules,
      loading,
      handleSignUp,
      goToLogin,
      User,
      Lock,
      Message
    }
  }
}
</script>

<style scoped>
.signup-page {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
}

.signup-card {
  width: 100%;
  max-width: 450px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 40px;
}

.signup-header {
  text-align: center;
  margin-bottom: 30px;
}

.signup-header h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 10px;
}

.signup-header p {
  color: #666;
  font-size: 1rem;
}

.signup-button {
  width: 100%;
  padding: 12px 0;
  font-size: 1.1rem;
}

.signup-footer {
  text-align: center;
  margin-top: 20px;
  color: #999;
  font-size: 0.9rem;
}

.signup-footer a {
  color: #409EFF;
  text-decoration: none;
}

@media (max-width: 768px) {
  .signup-card {
    padding: 20px;
  }
  
  .signup-header h2 {
    font-size: 1.5rem;
  }
}
</style>
