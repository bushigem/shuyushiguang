import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import ElementPlus from 'element-plus';
// --- 移除重复的 ElMessage 导入 ---
// import { ElMessage } from 'element-plus';
import 'element-plus/dist/index.css';
import axios from 'axios'

// --- 移除第一个 axiosInstance 声明和配置 (lines 9-23) ---
// const axiosInstance = axios.create({
//   baseURL: 'http://localhost:8000',
//   timeout: 5000,
//   headers: {
//     'Content-Type': 'application/json'
//   }
// });
//
// // 添加响应拦截器
// axiosInstance.interceptors.response.use(
//   response => response,
//   error => {
//     ElMessage.error('请求失败：' + error.message); // ElMessage 应该在组件中使用，而不是这里
//     return Promise.reject(error);
//   }
// );
// --- 移除结束 ---


const app = createApp(App);
// --- 移除全局挂载 (line 25) ---
// app.config.globalProperties.$axios = axiosInstance;
app.use(router);
app.use(ElementPlus); // ElementPlus 插件会自动处理 ElMessage 等组件的全局可用性

// --- 保留这个更完整的 Axios 实例创建和配置 ---
const axiosInstance = axios.create({
  // --- 确认 baseURL 正确 ---
  baseURL: 'http://127.0.0.1:8000', // 确保与后端服务器监听的地址一致
  timeout: 5000,
  // Content-Type 通常由 axios 根据数据自动设置，或者在需要时单独设置
  // headers: {
  //   'Content-Type': 'application/json'
  // }
});

// --- 添加请求拦截器以包含 Token ---
axiosInstance.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken');
  if (token) {
    // 注意 Django REST Framework Token Auth 需要 'Token ' 前缀
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// --- 添加响应拦截器进行全局错误处理 ---
axiosInstance.interceptors.response.use(response => {
  // 直接返回响应数据部分，如果后端总是包裹一层 data 的话
  // return response.data;
  // 或者返回整个响应对象
  return response;
}, error => {
   console.error('Axios Error:', error.response || error.message);
   // 可以在这里添加更具体的错误处理逻辑，例如 401 跳转登录
   if (error.response && error.response.status === 401) {
       console.warn('Unauthorized access detected.');
       // 清理无效 token 并跳转登录页
       localStorage.removeItem('authToken');
       // 触发全局事件或使用状态管理通知 App.vue 更新状态
       // window.dispatchEvent(new CustomEvent('auth-error'));
       // 或者直接跳转 (简单但不推荐在拦截器中直接操作路由)
       // window.location.href = '/login';
   }
   // 可以在这里使用 ElMessage 显示错误，但需要确保 ElementPlus 已完全加载
   // import { ElMessage } from 'element-plus'; // 在顶部导入
   // ElMessage.error(`请求错误: ${error.response?.data?.detail || error.message || '未知错误'}`);

  return Promise.reject(error); // 继续传递错误
});


app.mount('#app');

// --- 确保导出 axiosInstance ---
export { axiosInstance };