<template>
  <div class="book-detail-page" v-loading="loading">
    <el-page-header @back="goBack" content="图书详情" class="page-header">
    </el-page-header>

    <el-card v-if="book && !error" class="book-detail-card">
      <el-row :gutter="30">
        <!-- Book Cover -->
        <el-col :xs="24" :sm="8" :md="6" class="book-cover-col">
          <el-image
            :src="book.cover || require('@/assets/default-book-cover.jpg')"
            fit="contain"
            class="book-cover-image"
            lazy
          >
            <template #error>
              <div class="image-slot">
                <el-icon><Picture /></el-icon>
                <span>加载失败</span>
              </div>
            </template>
             <template #placeholder>
               <div class="image-slot">加载中...</div>
             </template>
          </el-image>
        </el-col>

        <!-- Book Info -->
        <el-col :xs="24" :sm="16" :md="18">
          <h1 class="book-title">{{ book.title }}</h1>
          <el-descriptions :column="2" border class="book-info-descriptions">
            <el-descriptions-item label="作者">{{ book.author || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="出版社">{{ book.publisher || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="出版日期">{{ book.publish_date || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="ISBN">{{ book.isbn || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="分类">
                <!-- 假设 book.category 是一个包含 id 和 name 的对象 -->
                {{ book.category?.name || '未分类' }}
            </el-descriptions-item>
             <el-descriptions-item label="馆藏位置">
                 <!-- 假设 book.location 是一个包含 id 和 name 的对象 -->
                 {{ book.location?.name || '未知' }}
             </el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="book.status === 'available' ? 'success' : 'warning'" size="small">
                {{ book.status === 'available' ? '可借阅' : '已借出' }}
              </el-tag>
            </el-descriptions-item>
             <el-descriptions-item label="总借阅次数">
                 {{ book.borrow_count || 0 }} 次
             </el-descriptions-item>
          </el-descriptions>

          <div class="book-description">
            <h3>内容简介</h3>
            <p>{{ book.description || '暂无简介' }}</p>
          </div>

          <!-- Action Buttons -->
          <div class="action-buttons">
            <el-button
              type="primary"
              size="large"
              :disabled="book.status !== 'available'"
              @click="borrowBook(book.id)"
            >
              <el-icon><Reading /></el-icon>
              立即借阅
            </el-button>
            <!-- 可以添加其他按钮，例如 "添加到收藏夹" 等 -->
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- Error State -->
    <el-empty v-if="error" :description="errorMessage"></el-empty>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage, ElMessageBox, ElPageHeader, ElCard, ElRow, ElCol, ElImage, ElDescriptions, ElDescriptionsItem, ElTag, ElButton, ElIcon, ElEmpty } from 'element-plus';
import { Picture, Reading } from '@element-plus/icons-vue'; // 引入图标

const route = useRoute();
const router = useRouter();

const book = ref(null);
const loading = ref(false);
const error = ref(false);
const errorMessage = ref('加载图书信息失败');

const fetchBookDetail = async () => {
  loading.value = true;
  error.value = false;
  const bookId = route.params.id; // 从路由获取 ID

  if (!bookId) {
    errorMessage.value = '无效的图书 ID';
    error.value = true;
    loading.value = false;
    return;
  }

  try {
    // --- 注意 API URL ---
    // 确保这个 URL 与后端获取单本书籍详情的路由匹配
    const response = await axios.get(`http://localhost:8000/api/books/books/${bookId}/`);
    // --- API URL 结束 ---

    // 检查返回的数据结构，可能需要根据实际情况调整
    if (response.data) {
      book.value = response.data;
       // 处理封面 URL，如果后端返回相对路径，可能需要拼接
       // 例如: book.value.cover = `http://localhost:8000${response.data.cover}`;
       // 这里假设后端直接返回了完整的 URL 或前端能处理的路径
    } else {
      throw new Error('未找到图书信息');
    }
  } catch (err) {
    console.error("获取图书详情失败:", err);
    error.value = true;
    if (err.response && err.response.status === 404) {
        errorMessage.value = '找不到指定的图书';
    } else {
        errorMessage.value = '加载图书信息失败，请稍后重试';
    }
    ElMessage.error(errorMessage.value);
  } finally {
    loading.value = false;
  }
};

// 借阅图书 (与 BookList.vue 类似，但可能需要根据用户登录状态等调整)
const borrowBook = (bookId) => {
  // 检查用户是否登录等逻辑...
  // ...

  ElMessageBox.confirm('确定要借阅这本书吗？', '借阅确认', {
    confirmButtonText: '确定借阅',
    cancelButtonText: '取消',
    type: 'info',
  }).then(async () => {
    try {
      // --- 调用借阅 API ---
      // 假设借阅 API 是 POST /api/borrowing/borrow/
      // 需要传递 book_id，后端需要能获取当前登录用户
      await axios.post(`http://localhost:8000/api/borrowing/borrow/`, { book_id: bookId });
      // --- API 调用结束 ---

      ElMessage.success('借阅成功！');
      // 借阅成功后更新本地图书状态
      if (book.value) {
        book.value.status = 'borrowed';
      }
      // 可以选择重新获取数据或仅更新状态
      // await fetchBookDetail();
    } catch (err) {
      console.error("借阅失败:", err);
      ElMessage.error(err.response?.data?.detail || '借阅失败，请稍后再试');
    }
  }).catch(() => {
    ElMessage.info('已取消借阅');
  });
};

const goBack = () => {
  router.back(); // 返回上一页
};

onMounted(() => {
  fetchBookDetail();
});
</script>

<style scoped>
.book-detail-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.book-detail-card {
  /* 卡片样式 */
}

.book-cover-col {
  display: flex;
  justify-content: center;
  align-items: flex-start; /* 封面图靠上对齐 */
}

.book-cover-image {
  width: 100%;
  max-width: 300px; /* 限制最大宽度 */
  height: auto; /* 高度自适应 */
  min-height: 200px; /* 最小高度，防止加载时塌陷 */
  border: 1px solid #ebeef5;
  border-radius: 4px;
  background-color: #f5f7fa; /* 占位背景色 */
}

.image-slot {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 200px; /* 与 min-height 保持一致或更大 */
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
  font-size: 14px;
}
.image-slot .el-icon {
  font-size: 30px;
  margin-bottom: 8px;
}


.book-title {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
}

.book-info-descriptions {
  margin-bottom: 20px;
}

.book-description {
  margin-top: 30px;
  margin-bottom: 30px;
}
.book-description h3 {
  margin-bottom: 10px;
  font-size: 18px;
}
.book-description p {
  line-height: 1.8;
  color: #606266;
  white-space: pre-wrap; /* 保留换行和空格 */
}

.action-buttons {
  margin-top: 20px;
  text-align: left; /* 按钮靠左 */
}
</style>