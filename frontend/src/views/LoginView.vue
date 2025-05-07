<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <span>用户登录</span>
        </div>
      </template>
      <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" @submit.prevent="handleLogin">
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            prefix-icon="User"
            clearable
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading" style="width: 100%;">
            {{ loading ? '登录中...' : '登 录' }}
          </el-button>
        </el-form-item>
         <!-- --- 添加注册链接 --- -->
         <div class="extra-links">
           <el-link type="primary" @click="goToRegister">没有账号？去注册</el-link>
           <!-- <el-link type="info" @click="forgotPassword">忘记密码？</el-link> -->
         </div>
         <!-- --- 链接结束 --- -->
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
// --- 导入 axiosInstance ---
import { axiosInstance } from '@/main'; // 使用配置好的实例
// --- 修改 Element Plus 导入，添加 ElLink ---
import { ElMessage, ElForm, ElFormItem, ElInput, ElButton, ElCard, ElLink } from 'element-plus';

const router = useRouter();
const loginFormRef = ref(null);
const loading = ref(false);

const loginForm = reactive({
  username: '',
  password: '',
});

const loginRules = reactive({
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
});

const handleLogin = async () => {
  if (!loginFormRef.value) return;

  loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      try {
        // --- 使用 axiosInstance ---
        const response = await axiosInstance.post('/api/auth/login/', {
          username: loginForm.username,
          password: loginForm.password,
        });

        if (response.data && response.data.token) {
          const token = response.data.token;
          localStorage.setItem('authToken', token);

          // --- 设置 axiosInstance 的 Header ---
          axiosInstance.defaults.headers.common['Authorization'] = `Token ${token}`;

          ElMessage.success('登录成功！');
          const redirectPath = router.currentRoute.value.query.redirect || '/';
          router.push(redirectPath);
        } else {
           throw new Error('登录失败，未获取到认证信息');
        }
      } catch (error) {
        console.error("登录失败:", error);
        let errorMessage = '登录失败，请稍后重试';
        if (error.response) {
          if (error.response.status === 400 && error.response.data) {
             errorMessage = error.response.data.non_field_errors?.[0] || '用户名或密码错误';
          } else if (error.response.status === 401) {
             errorMessage = '认证失败，请检查凭据';
          } else {
             errorMessage = `登录出错 (${error.response.status})`;
          }
        } else if (error.request) {
          errorMessage = '无法连接到服务器，请检查网络';
        } else {
          errorMessage = error.message || errorMessage;
        }
        ElMessage.error(errorMessage);
      } finally {
        loading.value = false;
      }
    } else {
      console.log('表单验证失败');
      return false;
    }
  });
};

// --- 添加跳转到注册页的函数 ---
const goToRegister = () => {
  router.push({ name: 'register' });
};
// const forgotPassword = () => { /* ... */ };
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 使容器占满整个视口高度 */
  background-color: #f0f2f5; /* 可选：添加背景色 */
}

.login-card {
  width: 400px;
}

.card-header {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
}

.extra-links {
  display: flex;
  justify-content: center; /* 让注册链接居中 */
  margin-top: 10px;
}
</style>