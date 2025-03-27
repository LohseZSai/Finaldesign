import axios from 'axios';
import { useAuthStore } from '../store/auth';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// 请求拦截器
api.interceptors.request.use(
  config => {
    const authStore = useAuthStore();
    // 如果有token，则添加到请求头
    if (authStore.token) {
      config.headers['Authorization'] = `Bearer ${authStore.token}`;
    }
    return config;
  },
  error => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data;
  },
  error => {
    const authStore = useAuthStore();
    
    // 如果是401错误，则清除token并跳转到登录页
    if (error.response && error.response.status === 401) {
      authStore.logout();
      window.location.href = '/login';
    }
    
    console.error('响应错误:', error);
    return Promise.reject(error);
  }
);

export default api; 