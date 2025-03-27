import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
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
    // 直接返回响应数据
    return response;
  },
  error => {
    if (error.response) {
      // 如果是401错误，则清除token并跳转到登录页
      if (error.response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('role');
        window.location.href = '/login';
      }
      
      // 处理422验证错误
      if (error.response.status === 422) {
        const validationErrors = error.response.data.detail || [];
        let errorMessage = '输入信息有误：\n';
        
        if (Array.isArray(validationErrors)) {
          validationErrors.forEach(err => {
            errorMessage += `${err.loc[1]}: ${err.msg}\n`;
          });
        } else {
          errorMessage = error.response.data.detail || '请检查输入信息';
        }
        
        error.message = errorMessage;
      }
    }
    
    console.error('响应错误:', error);
    return Promise.reject(error);
  }
);

export default api;
