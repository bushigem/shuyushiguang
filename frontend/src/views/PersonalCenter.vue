<template>
  <div class="personal-center">
    <!-- 顶部用户信息 -->
    <div class="user-info-header">
      <el-avatar :size="60" :src="userInfo.avatar || defaultAvatar" />
      <div class="user-details">
        <span class="username">{{ userInfo.username || '未登录' }}</span>
        <!-- 可以添加一个编辑按钮或链接 -->
        <el-button type="text" @click="editProfile" v-if="isLoggedIn">编辑资料</el-button>
      </div>
    </div>

    <!-- 标签页 -->
    <el-tabs v-model="activeTab" class="content-tabs">
      <el-tab-pane label="当前借阅" name="currentBorrows">
        <div v-if="currentBorrows.length > 0" class="borrow-list">
           <el-row :gutter="20">
             <el-col v-for="borrow in currentBorrows" :key="borrow.id" :xs="24" :sm="12" :md="8" :lg="6">
               <el-card class="borrow-card" shadow="hover">
                 <div class="borrow-card-content">
                   <el-image :src="borrow.book.cover || defaultBookCover" fit="cover" class="borrow-cover"/>
                   <div class="borrow-info">
                     <h4 class="book-title">{{ borrow.book.title }}</h4>
                     <p class="book-author">{{ borrow.book.author }}</p>
                     <p>借阅日期: {{ formatDate(borrow.borrow_date) }}</p>
                     <p>
                       应还日期:
                       <el-tag :type="getDueDateTagType(borrow.due_date)" size="small">
                         {{ formatDate(borrow.due_date) }}
                       </el-tag>
                     </p>
                     <el-button
                       type="primary"
                       size="small"
                       @click="renewBook(borrow.id)"
                       :disabled="!borrow.can_renew"
                       class="renew-button"
                     >
                       续借
                     </el-button>
                   </div>
                 </div>
               </el-card>
             </el-col>
           </el-row>
        </div>
        <el-empty v-else description="暂无当前借阅记录"></el-empty>
      </el-tab-pane>

      <el-tab-pane label="借阅历史" name="borrowHistory">
        <el-table :data="borrowHistory" style="width: 100%" v-loading="historyLoading">
          <el-table-column prop="book.title" label="书名" />
          <el-table-column prop="book.author" label="作者" />
          <el-table-column prop="borrow_date" label="借阅日期">
             <template #default="scope">{{ formatDate(scope.row.borrow_date) }}</template>
          </el-table-column>
          <el-table-column prop="return_date" label="归还日期">
             <template #default="scope">{{ formatDate(scope.row.return_date) }}</template>
          </el-table-column>
        </el-table>
        <el-pagination
          v-if="historyTotal > historyPageSize"
          v-model:current-page="historyCurrentPage"
          :page-size="historyPageSize"
          :total="historyTotal"
          @current-change="handleHistoryPageChange"
          layout="prev, pager, next"
          background
          class="pagination"
        />
        <el-empty v-if="!historyLoading && borrowHistory.length === 0" description="暂无借阅历史记录"></el-empty>
      </el-tab-pane>

      <el-tab-pane label="账户设置" name="accountSettings">
        <el-form ref="accountFormRef" :model="accountForm" :rules="accountRules" label-width="100px" style="max-width: 500px">
          <el-form-item label="当前密码" prop="currentPassword">
            <el-input type="password" v-model="accountForm.currentPassword" show-password />
          </el-form-item>
          <el-form-item label="新密码" prop="newPassword">
            <el-input type="password" v-model="accountForm.newPassword" show-password />
          </el-form-item>
          <el-form-item label="确认新密码" prop="confirmPassword">
            <el-input type="password" v-model="accountForm.confirmPassword" show-password />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitAccountForm">保存修改</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import axios from 'axios'; // 假设你配置了 axios

// --- 响应式状态 ---
const activeTab = ref('currentBorrows');
const defaultAvatar = '/default-avatar.png'; // 默认头像路径
const defaultBookCover = '/default-book-cover.jpg'; // 默认图书封面路径

// 用户信息 (需要从状态管理或 API 获取)
const userInfo = ref({
  id: 1,
  username: '测试用户',
  avatar: '' // 可以是 URL
});
const isLoggedIn = computed(() => !!userInfo.value.id); // 简单判断是否登录

// 当前借阅
const currentBorrows = ref([]);

// 借阅历史
const borrowHistory = ref([]);
const historyLoading = ref(false);
const historyCurrentPage = ref(1);
const historyPageSize = ref(10);
const historyTotal = ref(0);

// 账户设置
const accountFormRef = ref(null);
const accountForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
});

// --- 方法 ---

// 格式化日期 (简单示例)
const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString();
};

// 根据应还日期获取 Tag 类型
const getDueDateTagType = (dueDateString) => {
  if (!dueDateString) return 'info';
  const dueDate = new Date(dueDateString);
  const today = new Date();
  today.setHours(0, 0, 0, 0); // 忽略时间部分
  const diffDays = Math.ceil((dueDate - today) / (1000 * 60 * 60 * 24));

  if (diffDays < 0) return 'danger'; // 已超期
  if (diffDays <= 3) return 'warning'; // 即将到期
  return 'success'; // 正常
};

// 获取当前借阅数据 (示例 API 调用)
const fetchCurrentBorrows = async () => {
  try {
    // --- 取消注释实际 API 调用 ---
    const response = await axios.get('/api/user/borrows/current'); // 使用 axios
    currentBorrows.value = response.data;
    // --- 删除或注释掉模拟数据 ---
    /*
    currentBorrows.value = [
      { id: 1, borrow_date: '2023-10-01T10:00:00Z', due_date: '2023-10-15T10:00:00Z', can_renew: true, book: { id: 101, title: '深入理解计算机系统', author: 'Randal E. Bryant', cover: '/covers/cover1.jpg' } },
      { id: 2, borrow_date: '2023-10-05T14:30:00Z', due_date: '2023-10-19T14:30:00Z', can_renew: false, book: { id: 102, title: '代码整洁之道', author: 'Robert C. Martin', cover: '/covers/cover2.jpg' } },
      { id: 3, borrow_date: '2023-10-10T09:00:00Z', due_date: '2023-10-13T09:00:00Z', can_renew: true, book: { id: 103, title: '三体', author: '刘慈欣', cover: null } }, // 测试默认封面
       { id: 4, borrow_date: '2023-09-20T09:00:00Z', due_date: '2023-10-04T09:00:00Z', can_renew: true, book: { id: 104, title: '人类简史', author: '尤瓦尔·赫拉利', cover: '/covers/cover4.jpg' } }, // 测试超期
    ];
    */
  } catch (error) {
    console.error("获取当前借阅失败:", error);
    ElMessage.error('获取当前借阅记录失败');
  }
};

// 获取借阅历史数据 (示例 API 调用)
const fetchBorrowHistory = async (page = 1) => {
  historyLoading.value = true;
  try {
    // --- 取消注释实际 API 调用 ---
    const response = await axios.get('/api/user/borrows/history', { // 使用 axios
      params: { page: page, page_size: historyPageSize.value }
    });
    borrowHistory.value = response.data.results;
    historyTotal.value = response.data.count;
    // --- 删除或注释掉模拟数据 ---
    /*
    const total = 25;
    const start = (page - 1) * historyPageSize.value;
    const end = start + historyPageSize.value;
    const mockData = Array.from({ length: total }, (_, i) => ({
      id: 200 + i,
      borrow_date: `2023-0${9-Math.floor(i/5)}-${28-i%28}T10:00:00Z`,
      return_date: `2023-0${9-Math.floor(i/5)}-${29-i%28}T15:00:00Z`,
      book: { id: 200 + i, title: `历史书籍 ${i + 1}`, author: `作者 ${i + 1}` }
    }));
    await new Promise(resolve => setTimeout(resolve, 500)); // 模拟网络延迟
    borrowHistory.value = mockData.slice(start, end);
    historyTotal.value = total;
    */
  } catch (error) {
    console.error("获取借阅历史失败:", error);
    ElMessage.error('获取借阅历史记录失败');
    borrowHistory.value = [];
    historyTotal.value = 0;
  } finally {
    historyLoading.value = false;
  }
};

// 历史记录分页改变
const handleHistoryPageChange = (page) => {
  fetchBorrowHistory(page);
};

// 续借图书 (示例)
const renewBook = async (borrowId) => { // borrowId 现在会被使用
   ElMessageBox.confirm('确定要续借这本书吗？', '续借确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
      try {
        // --- 取消注释实际 API 调用，并使用 borrowId ---
        await axios.post(`/api/borrows/${borrowId}/renew/`); // 使用 axios 和 borrowId
        ElMessage.success('续借成功！');
        // 续借成功后刷新当前借阅列表
        await fetchCurrentBorrows();
      } catch (error) {
        console.error("续借失败:", error);
        // 根据后端返回显示具体错误信息
        ElMessage.error(error.response?.data?.detail || '续借失败，请稍后再试');
      }
  }).catch(() => {
    // 用户取消
  });
};

// 编辑资料 (示例，通常会导航到单独页面或打开弹窗)
const editProfile = () => {
  ElMessage.info('跳转到编辑资料页面（待实现）');
  // router.push('/profile/edit'); // 或者打开一个对话框
};

// 账户设置表单验证规则
const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入新密码'));
  } else {
    if (accountForm.confirmPassword !== '') {
      if (!accountFormRef.value) return;
      accountFormRef.value.validateField('confirmPassword', () => null);
    }
    callback();
  }
};
const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入新密码'));
  } else if (value !== accountForm.newPassword) {
    callback(new Error("两次输入的新密码不一致!"));
  } else {
    callback();
  }
};

const accountRules = reactive({
  currentPassword: [{ required: true, message: '请输入当前密码', trigger: 'blur' }],
  newPassword: [
    { required: true, validator: validatePass, trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validatePass2, trigger: 'blur' }
  ],
});

// 提交账户设置表单 (示例)
const submitAccountForm = async () => {
  if (!accountFormRef.value) return;
  await accountFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // --- 取消注释实际 API 调用 ---
        await axios.post('/api/user/change-password', { // 使用 axios
          current_password: accountForm.currentPassword,
          new_password: accountForm.newPassword,
        });
        ElMessage.success('密码修改成功！');
        accountFormRef.value.resetFields(); // 清空表单
      } catch (error) {
         console.error("修改密码失败:", error);
         ElMessage.error(error.response?.data?.detail || '密码修改失败，请检查当前密码是否正确');
      }
    } else {
      console.log('表单验证失败!');
      return false;
    }
  });
};


// --- 生命周期钩子 ---
onMounted(() => {
  // 页面加载时获取数据
  fetchCurrentBorrows();
  fetchBorrowHistory(historyCurrentPage.value);
  // 获取用户信息 (如果需要)
  // fetchUserInfo();
});

</script>

<style scoped>
.personal-center {
  padding: 20px;
}

.user-info-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.user-details {
  margin-left: 15px;
  display: flex;
  flex-direction: column;
}

.username {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
}

.content-tabs {
  margin-top: 20px;
}

.borrow-list {
  margin-top: 10px;
}

.borrow-card {
  margin-bottom: 20px;
}

.borrow-card-content {
  display: flex;
}

.borrow-cover {
  width: 80px;
  height: 110px;
  object-fit: cover;
  margin-right: 15px;
  flex-shrink: 0; /* 防止图片被压缩 */
}

.borrow-info {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.borrow-info h4 {
  margin: 0 0 5px 0;
  font-size: 15px;
}
.borrow-info p {
  font-size: 13px;
  color: #606266;
  margin: 3px 0;
}

.renew-button {
  margin-top: auto; /* 将按钮推到底部 */
  align-self: flex-start; /* 左对齐 */
}


.pagination {
  margin-top: 20px;
  text-align: center;
}
</style>