import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import BookList from '@/views/BookList.vue'
import PersonalCenter from '@/views/PersonalCenter.vue'
import BookDetail from '@/views/BookDetail.vue'
import LoginView from '@/views/LoginView.vue'
// --- 导入注册组件 ---
import RegisterView from '@/views/RegisterView.vue' // 确认导入路径和名称正确

const routes = [
  { path: '/', name: 'home', component: HomePage },
  { path: '/login', name: 'login', component: LoginView, meta: { guest: true } },
  // --- 添加注册路由 ---
  {
    path: '/register', // 确认路径
    name: 'register', // 确认名称
    component: RegisterView, // 确认组件
    meta: { guest: true } // 确认元信息
  },
  // --- 其他路由 ---
  { path: '/booklist', name: 'booklist', component: BookList, meta: { requiresAuth: false } },
  { path: '/personalcenter', name: 'personalcenter', component: PersonalCenter, meta: { requiresAuth: true } },
  { path: '/book/:id', name: 'bookDetail', component: BookDetail, props: true, meta: { requiresAuth: false } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// --- 导航守卫 (保持不变) ---
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('authToken');

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'login', query: { redirect: to.fullPath } });
    } else {
      next();
    }
  } else if (to.matched.some(record => record.meta.guest)) {
     if (isAuthenticated && to.name !== 'home') { // 如果已登录，访问访客页（非首页）则跳首页
       next({ name: 'home' });
     } else {
       next();
     }
  } else {
    next();
  }
});
// --- 守卫结束 ---

export default router