<template>
  <div class="login-page">
    <Navbar />
    
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h2>员工登录</h2>
          <p>欢迎使用泓泰生物科技智能养殖管理系统</p>
        </div>
        
        <el-form
          ref="loginForm"
          :model="loginForm"
          :rules="loginRules"
          label-position="top"
          @submit.prevent="handleLogin"
        >
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              prefix-icon="User"
            />
          </el-form-item>
          
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>
          
          <div class="remember-forgot">
            <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
            <el-button type="text" @click="forgotPassword">忘记密码?</el-button>
          </div>
          
          <el-form-item>
            <el-button
              type="primary"
              native-type="submit"
              :loading="loading"
              class="login-button"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="divider">
          <span>或</span>
        </div>
        
        <div class="oauth-login">
          <el-button
            type="default"
            class="github-button"
            @click="handleGithubLogin"
            :loading="githubLoading"
          >
            <i class="el-icon-platform-eleme"></i>
            使用GitHub账号登录
          </el-button>
        </div>
        
        <div class="login-footer">
          <p>遇到问题? 请联系 <a href="mailto:support@hongtai-bio.com">技术支持</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'
import { useAuth0 } from '@auth0/auth0-vue'
import Navbar from '@/components/layout/Navbar.vue'

export default {
  name: 'LoginPage',
  components: {
    Navbar
  },
  
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const auth0 = useAuth0()
    const loginForm = ref(null)
    
    const formData = reactive({
      username: '',
      password: '',
      remember: false
    })
    
    const loading = ref(false)
    const githubLoading = ref(false)
    
    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度应为3-20个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少为6个字符', trigger: 'blur' }
      ]
    }
    
    const handleLogin = async () => {
      if (!loginForm.value) return
      
      await loginForm.value.validate(async (valid) => {
        if (valid) {
          try {
            loading.value = true
            
            const result = await authStore.login({
              username: formData.username,
              password: formData.password,
              remember: formData.remember
            })
            
            if (result.success) {
              ElMessage.success('登录成功')
              router.push('/admin')
            } else {
              ElMessage.error(result.message)
            }
          } catch (error) {
            console.error('登录错误:', error)
            ElMessage.error('登录失败，请稍后再试')
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    const handleGithubLogin = async () => {
      try {
        githubLoading.value = true
        await auth0.loginWithRedirect({
          authorizationParams: {
            connection: 'github'
          }
        })
      } catch (error) {
        console.error('GitHub登录错误:', error)
        ElMessage.error('GitHub登录失败，请稍后再试')
        githubLoading.value = false
      }
    }
    
    const forgotPassword = () => {
      ElMessage.info('请联系系统管理员重置密码')
    }
    
    return {
      loginForm,
      loginForm: formData,
      loginRules,
      loading,
      githubLoading,
      handleLogin,
      handleGithubLogin,
      forgotPassword
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
}

.login-card {
  width: 100%;
  max-width: 450px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 40px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 10px;
}

.login-header p {
  color: #666;
  font-size: 1rem;
}

.remember-forgot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
  padding: 12px 0;
  font-size: 1.1rem;
}

.divider {
  display: flex;
  align-items: center;
  margin: 20px 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #eee;
}

.divider span {
  padding: 0 10px;
  color: #999;
  font-size: 0.9rem;
}

.oauth-login {
  margin-bottom: 20px;
}

.github-button {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.login-footer {
  text-align: center;
  margin-top: 20px;
  color: #999;
  font-size: 0.9rem;
}

.login-footer a {
  color: #409EFF;
  text-decoration: none;
}
</style> 