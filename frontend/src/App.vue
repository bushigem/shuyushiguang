<template>
  <el-container class="app-container">
    <el-header class="app-header" height="60px">
      <div class="header-content">
        <!-- Logo -->
        <div class="logo" @click="goHome">书语时光</div>

        <!-- Navigation Menu -->
        <el-menu
          :default-active="activeMenu"
          class="header-menu"
          mode="horizontal"
          router
          :ellipsis="false"
        >
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/booklist">图书列表</el-menu-item>
          <!-- 如果个人中心也应作为主导航项 -->
          <!-- <el-menu-item v-if="isLoggedIn" index="/personalcenter">个人中心</el-menu-item> -->
        </el-menu>

        <!-- Spacer -->
        <div class="header-spacer"></div>

        <!-- Search Input -->
        <div class="search-container">
           <el-input
             v-model="searchQuery"
             placeholder="搜索图书..."
             clearable
             @keyup.enter="handleSearch"
             class="search-input"
           >
             <template #append>
               <el-button :icon="Search" @click="handleSearch" />
             </template>
           </el-input>
        </div>

        <!-- --- 添加 header-right-area 类 --- -->
        <!-- User Area -->
        <div class="user-area header-right-area">
          <template v-if="isLoggedIn">
            <el-dropdown @command="handleUserCommand">
              <!-- TODO: 从真实 userInfo 获取头像 -->
              <el-avatar :size="32" :src="userInfo.avatar || defaultAvatar" class="user-avatar" />
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button type="primary" plain @click="login">登录</el-button>
            <el-button @click="register">注册</el-button>
          </template>
        </div>
      </div>
    </el-header>

    <!-- Main Content Area -->
    <el-main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>

    <!-- Footer -->
    <el-footer class="app-footer" height="40px">
      © {{ new Date().getFullYear() }} 书语时光
    </el-footer>

    <!-- 添加悬浮聊天窗口 -->
    <FloatingChatWindow />
  </el-container>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'; // 引入 onMounted
import { useRouter, useRoute } from 'vue-router';
import { Search } from '@element-plus/icons-vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import FloatingChatWindow from '@/components/FloatingChatWindow.vue';
import { axiosInstance } from '@/main'; // 导入 axios 实例

const router = useRouter();
const route = useRoute();

// --- State ---
const activeMenu = ref('/');
const searchQuery = ref('');
const defaultAvatar = '/default-avatar.png'; // 确保这个路径是正确的

// --- 认证状态 ---
// 直接从 localStorage 初始化登录状态
const isLoggedIn = ref(!!localStorage.getItem('authToken'));
// TODO: 登录后从后端获取真实用户信息
const userInfo = ref({
  username: '',
  avatar: ''
});

// --- Watchers ---
watch(() => route.path, (newPath) => {
  // 更新激活菜单项
  if (newPath === '/') {
    activeMenu.value = '/';
  } else if (newPath.startsWith('/booklist')) {
    activeMenu.value = '/booklist';
  } else if (newPath.startsWith('/personalcenter')) {
    // 如果个人中心在主导航，取消注释下一行
    // activeMenu.value = '/personalcenter';
  } else {
    // 对于登录、注册等非主导航页面，保持之前的激活项或设为根路径
    // activeMenu.value = '/'; // 或者保持不变
  }

  // 如果不在图书列表页，清空搜索框
  if (!newPath.startsWith('/booklist')) {
     searchQuery.value = '';
  }

  // 每次路由变化后，再次确认登录状态（以防 localStorage 被外部修改）
  isLoggedIn.value = !!localStorage.getItem('authToken');
  // TODO: 如果已登录，可以考虑在这里获取最新的用户信息

}, { immediate: true });

watch(() => route.query.search, (newSearchQuery) => {
    if (route.path.startsWith('/booklist')) {
        searchQuery.value = newSearchQuery || '';
    }
}, { immediate: true });


// --- Methods ---
const goHome = () => {
  router.push('/');
};

const handleSearch = () => {
  if (route.path !== '/booklist' || route.query.search !== searchQuery.value) {
      router.push({ path: '/booklist', query: { search: searchQuery.value || undefined } });
  }
};

// --- 更新 login 方法 ---
const login = () => {
  // 跳转到登录页面
  router.push('/login');
};

// --- 更新 register 方法 ---
const register = () => {
  // 跳转到注册页面
  router.push('/register');
};

// --- 更新 logout 逻辑 ---
const performLogout = () => {
  localStorage.removeItem('authToken');
  // 清除 axios 的默认 header
  delete axiosInstance.defaults.headers.common['Authorization'];
  isLoggedIn.value = false; // 更新状态
  userInfo.value = {}; // 清空用户信息
  ElMessage.success('已退出登录');
  router.push({ name: 'login' }); // 跳转到登录页
};

const handleUserCommand = (command) => {
  if (command === 'profile') {
    router.push('/personalcenter');
  } else if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }).then(() => {
      performLogout(); // 执行实际的退出操作
    }).catch(() => {
      // 用户取消
      ElMessage.info('已取消退出');
    });
  }
};

// --- 生命周期钩子 ---
onMounted(() => {
  // 组件挂载时再次确认登录状态
  isLoggedIn.value = !!localStorage.getItem('authToken');
  // TODO: 如果已登录，可以在这里触发获取用户信息的请求
  // if (isLoggedIn.value) {
  //   fetchUserInfo();
  // }
});

// 监听 storage 事件，以便在其他标签页登出时同步状态（可选）
// window.addEventListener('storage', (event) => {
//   if (event.key === 'authToken') {
//     isLoggedIn.value = !!event.newValue;
//     if (!isLoggedIn.value) {
//        userInfo.value = {};
//        // 可能需要强制跳转到登录页
//        router.push('/login');
//     }
//   }
// });

</script>

<style>
/* Global Styles & Resets */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f7fa;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background-color: #ffffff;
  border-bottom: 1px solid #e0e0e0;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.header-content {
  display: flex;
  align-items: center;
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  font-size: 22px;
  font-weight: bold;
  color: var(--el-color-primary);
  cursor: pointer;
  margin-right: 40px;
}

.header-menu {
  border-bottom: none; /* 移除菜单底边框 */
  height: 100%;
}
.header-menu .el-menu-item {
    height: 100%;
    display: inline-flex;
    align-items: center;
    border-bottom: none; /* 移除菜单项底边框 */
    padding-bottom: 0; /* 移除可能存在的内边距 */
    line-height: 60px; /* 确保与 header 高度一致 */
}
.header-menu .el-menu-item:hover {
    background-color: #f5f7fa; /* 保持 hover 效果 */
}
/* 提高激活状态选择器的优先级，尝试避免 !important */
.header-menu.el-menu--horizontal > .el-menu-item.is-active {
    border-bottom: 2px solid var(--el-color-primary);
    color: var(--el-color-primary);
    background-color: #fff; /* 确保激活时背景不是 hover 颜色 */
}


.header-spacer {
  flex-grow: 1;
}

.search-container {
    margin-right: 20px;
}
.search-input {
  width: 250px;
}
.search-input .el-input-group__append {
    background-color: var(--el-color-primary);
    color: white;
    border-color: var(--el-color-primary);
}
.search-input .el-input-group__append .el-button {
    color: white;
}
.search-input .el-input-group__append .el-button:hover {
    background-color: var(--el-color-primary-light-3);
}

/* --- 使用类选择器替代依赖内联样式的选择器 --- */
.header-right-area {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  cursor: pointer;
  border: 1px solid #eee;
}

.app-main {
  flex-grow: 1;
  padding: 20px;
  margin-top: 60px; /* 为固定 header 留出空间 */
  background-color: #ffffff;
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  box-sizing: border-box;
}

.app-footer {
  text-align: center;
  line-height: 40px;
  color: #909399;
  font-size: 12px;
  background-color: #f5f7fa;
  border-top: 1px solid #e0e0e0;
  width: 100%;
}

/* Router Transition */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

</style>