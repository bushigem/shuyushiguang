<template>
  <div class="register-container">
    <el-card class="register-card">
      <template #header>
        <div class="card-header">
          <span>用户注册</span>
        </div>
      </template>
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-position="top"
        @submit.prevent="handleRegister"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="registerForm.username" placeholder="请输入用户名" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="registerForm.name" placeholder="请输入真实姓名" clearable />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
           <el-col :span="12">
             <el-form-item label="学号/工号" prop="student_id">
               <el-input v-model="registerForm.student_id" placeholder="请输入学号或工号" clearable />
             </el-form-item>
           </el-col>
           <el-col :span="12">
             <el-form-item label="邮箱" prop="email">
               <el-input v-model="registerForm.email" placeholder="请输入邮箱" type="email" clearable />
             </el-form-item>
           </el-col>
         </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="密码" prop="password">
              <el-input v-model="registerForm.password" type="password" placeholder="请输入密码" show-password clearable />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input v-model="registerForm.confirmPassword" type="password" placeholder="请再次输入密码" show-password clearable />
            </el-form-item>
          </el-col>
        </el-row>

         <el-row :gutter="20">
           <el-col :span="12">
             <el-form-item label="手机号" prop="phone">
               <el-input v-model="registerForm.phone" placeholder="请输入手机号" clearable />
             </el-form-item>
           </el-col>
           <el-col :span="12">
             <el-form-item label="部门/学院" prop="department">
               <el-input v-model="registerForm.department" placeholder="请输入部门或学院" clearable />
             </el-form-item>
           </el-col>
         </el-row>
         <!-- 注意：角色(role)通常不应由用户在注册时指定，默认为 'student' 或由后端逻辑决定 -->

        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading" style="width: 100%;">
            {{ loading ? '注册中...' : '注 册' }}
          </el-button>
        </el-form-item>

        <div class="extra-links">
          <el-link type="primary" @click="goToLogin">已有账号？去登录</el-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElForm, ElFormItem, ElInput, ElButton, ElCard, ElRow, ElCol, ElLink } from 'element-plus';
import { axiosInstance } from '@/main'; // 导入在 main.js 中配置的 axios 实例

const router = useRouter();
const registerFormRef = ref(null);
const loading = ref(false);

// 注册表单数据模型 (字段需与 UserCreateSerializer 对应)
const registerForm = reactive({
  username: '',
  name: '',
  student_id: '', // 学号/工号
  email: '',
  phone: '',
  department: '',
  password: '',
  confirmPassword: '',
  // role: 'student' // 默认角色可以在后端设置，或如果需要前端传，则添加此字段
});

// 自定义密码验证规则
const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'));
  } else {
    if (registerForm.confirmPassword !== '') {
      // 触发表单的确认密码验证
      if (!registerFormRef.value) return;
      registerFormRef.value.validateField('confirmPassword', () => null);
    }
    callback();
  }
};
const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'));
  } else if (value !== registerForm.password) {
    callback(new Error("两次输入的密码不一致!"));
  } else {
    callback();
  }
};

// 表单验证规则
const registerRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  name: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
  student_id: [{ required: true, message: '请输入学号或工号', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
  ],
   phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }], // 可以添加更严格的手机号格式校验
   department: [{ required: true, message: '请输入部门或学院', trigger: 'blur' }],
  password: [
    { required: true, validator: validatePass, trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validatePass2, trigger: 'blur' }
  ],
});

const handleRegister = async () => {
  if (!registerFormRef.value) return;

  registerFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      try {
        // --- 准备要发送的数据 ---
        // 移除确认密码字段，因为它不需要发送给后端
        // eslint-disable-next-line no-unused-vars
        const { confirmPassword, ...postData } = registerForm; // <--- 在这行上面添加注释
        // 如果角色不由用户指定，确保不发送 role 字段，或由后端处理默认值

        // --- 发送注册请求 ---
        // !!! 重要：这里的 URL 需要替换为你后端实际的公共注册 API 端点 !!!
        await axiosInstance.post('/api/auth/register/', postData);
        // --- 请求结束 ---

        ElMessage.success('注册成功！即将跳转到登录页面...');
        // 注册成功后跳转到登录页
        setTimeout(() => {
          router.push({ name: 'login' });
        }, 1500);

      } catch (error) {
        console.error("注册失败:", error);
        let errorMessage = '注册失败，请稍后重试';
        if (error.response && error.response.data) {
          // 尝试解析后端返回的详细错误信息
          const errors = error.response.data;
          // 检查常见的错误字段
          if (errors.username) {
            errorMessage = `用户名错误: ${errors.username.join(', ')}`;
          } else if (errors.email) {
            errorMessage = `邮箱错误: ${errors.email.join(', ')}`;
          } else if (errors.password) {
             errorMessage = `密码错误: ${errors.password.join(', ')}`;
          } else if (errors.non_field_errors) {
             errorMessage = errors.non_field_errors.join(', ');
          } else {
             // 其他可能的错误格式
             errorMessage = JSON.stringify(errors);
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
      ElMessage.error('请检查输入项是否正确');
      return false;
    }
  });
};

const goToLogin = () => {
  router.push({ name: 'login' });
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh; /* 使用 min-height 保证内容多时也能正常显示 */
  padding: 20px 0; /* 上下留白 */
  background-color: #f0f2f5;
}

.register-card {
  width: 600px; /* 注册表单通常需要更宽 */
  max-width: 90%; /* 移动端适配 */
}

.card-header {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
}

.extra-links {
  text-align: center;
  margin-top: 10px;
}
</style>