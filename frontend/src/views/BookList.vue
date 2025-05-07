<template>
  <div class="book-list-page">
    <!-- Filter and Sort Section -->
    <el-card class="filter-card" shadow="never">
      <el-form :inline="true" :model="filterParams" class="filter-form">
        <el-form-item label="分类">
          <el-select v-model="filterParams.category" placeholder="所有分类" clearable @change="handleFilterChange">
            <el-option label="所有分类" value=""></el-option>
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="filterParams.status" @change="handleFilterChange">
            <el-radio-button :value="null">全部</el-radio-button>
            <el-radio-button :value="'available'">可借阅</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="排序">
          <el-select v-model="filterParams.ordering" @change="handleFilterChange">
            <el-option label="按出版日期" value="-publish_date"></el-option>
            <el-option label="按热度" value="-borrow_count"></el-option>
             <el-option label="按书名" value="title"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item class="view-toggle">
           <el-button-group>
             <el-tooltip content="网格视图" placement="top">
               <el-button :type="viewMode === 'grid' ? 'primary' : ''" :icon="Grid" @click="viewMode = 'grid'" />
             </el-tooltip>
              <el-tooltip content="列表视图" placement="top">
               <el-button :type="viewMode === 'list' ? 'primary' : ''" :icon="List" @click="viewMode = 'list'" />
              </el-tooltip>
           </el-button-group>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Books Display Area -->
    <div class="books-display-area" v-loading="loading">
      <!-- Grid View -->
      <el-row :gutter="20" v-if="viewMode === 'grid'">
        <el-col
          v-for="book in books"
          :key="book.id"
          :xs="12" :sm="8" :md="6" :lg="4" :xl="4"
          class="book-col"
        >
          <BookCard :book="book" @click="goToBookDetail(book.id)" />
        </el-col>
      </el-row>

      <!-- List View -->
      <el-table :data="books" stripe style="width: 100%" v-else>
         <el-table-column label="封面" width="80">
            <template #default="scope">
              <el-image
                :src="scope.row.cover || require('@/assets/default-book-cover.jpg')"
                fit="cover"
                style="width: 50px; height: 70px; vertical-align: middle;"
                lazy
              />
            </template>
          </el-table-column>
        <el-table-column prop="title" label="书名" sortable />
        <el-table-column prop="author" label="作者" sortable />
        <el-table-column prop="publisher" label="出版社" />
        <el-table-column prop="isbn" label="ISBN" />
        <el-table-column label="状态" width="100">
           <template #default="scope">
             <el-tag :type="scope.row.status === 'available' ? 'success' : 'warning'" size="small">
               {{ scope.row.status === 'available' ? '可借阅' : '已借出' }}
             </el-tag>
           </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button size="small" @click="goToBookDetail(scope.row.id)">详情</el-button>
            <el-button
              type="primary"
              size="small"
              :disabled="scope.row.status !== 'available'"
              @click="borrowBook(scope.row.id)"
            >
              借阅
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Empty State -->
      <el-empty v-if="!loading && books.length === 0" description="未找到符合条件的图书"></el-empty>
    </div>

    <!-- Pagination -->
    <el-pagination
      v-if="totalBooks > pageSize"
      v-model:current-page="currentPage"
      :page-size="pageSize"
      :total="totalBooks"
      layout="prev, pager, next, jumper, ->, total"
      @current-change="handlePageChange"
      background
      class="pagination-container"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios'; // 确保已安装并配置 axios
import { Grid, List } from '@element-plus/icons-vue';
import { ElMessage, ElMessageBox } from 'element-plus'; // 引入 ElMessageBox
import BookCard from '@/components/BookCard.vue';

const router = useRouter();
const route = useRoute();

// --- State ---
const books = ref([]);
const categories = ref([]);
const viewMode = ref('grid');
const currentPage = ref(1);
const pageSize = ref(12); // 网格视图每页显示数量，可根据需要调整
const totalBooks = ref(0);
const loading = ref(false);

// Filter and Sort Parameters (使用 reactive)
const filterParams = reactive({
  category: '',
  status: null,  // 修改这里，从空字符串改为 null
  ordering: '-publish_date',
  search: route.query.search || '' // 从路由初始化搜索词
});

// --- Methods ---
const fetchCategories = async () => {
  try {
    // 替换为你的实际 API 端点
    // const response = await axios.get('/api/categories/');
    // categories.value = response.data;
     // --- Mock Data ---
    await new Promise(resolve => setTimeout(resolve, 100)); // 模拟延迟
    categories.value = [
      { id: 1, name: '文学' },
      { id: 2, name: '科技' },
      { id: 3, name: '历史' },
      { id: 4, name: '艺术' },
    ];
     // --- Mock Data End ---
  } catch (error) {
    console.error("获取分类失败:", error);
    ElMessage.error('获取分类列表失败');
  }
};

// 获取图书列表
const fetchBooks = async (page = 1) => {
  loading.value = true;
  currentPage.value = page;

  try {
    const response = await axios({
      method: 'get',
      // --- 修改这里的 URL ---
      url: 'http://localhost:8000/api/books/books/', // <--- 在末尾添加 'books/'
      // --- 修改结束 ---
      params: {
        page: currentPage.value,
        page_size: pageSize.value,
        ordering: filterParams.ordering,
        ...(filterParams.category && { category: filterParams.category }),
        ...(filterParams.status && { status: filterParams.status }),
        ...(filterParams.search && { search: filterParams.search })
      }
    });

    console.log('API响应:', response.data);

    // 主要检查 response.data.results 是否是有效的数组
    if (response.data && Array.isArray(response.data.results)) {
      // 确认是分页响应，使用 results 和 count
      books.value = response.data.results.map(book => ({
        ...book,
        // 处理封面，如果 cover 是 null 或空字符串，使用默认图片
        cover: book.cover ? book.cover : require('@/assets/default-book-cover.jpg')
      }));
      totalBooks.value = response.data.count;
    } else {
      // 如果响应结构不符合预期 (不是分页格式)，则清空列表并记录错误
      console.error("获取的数据格式不正确或非分页格式:", response.data);
      books.value = [];
      totalBooks.value = 0;
      // 可以选择性地显示错误消息
      // ElMessage.error('获取书籍列表失败，数据格式错误');
    }
    // --- 修改结束 ---

  } catch (error) {
    console.error("获取图书列表失败:", error);
    if (error.response) {
      console.error("错误状态:", error.response.status);
      console.error("错误数据:", error.response.data);
    }
    ElMessage.error('获取图书列表失败: ' + (error.response?.data?.detail || error.message));
    books.value = [];
    totalBooks.value = 0;
  } finally {
    loading.value = false;
  }
};

// 处理筛选/排序条件变化
const handleFilterChange = () => {
  // 当筛选或排序条件改变时，总是回到第一页
  fetchBooks(1);
};

// 处理分页变化
const handlePageChange = (page) => {
  fetchBooks(page);
};

// 跳转到图书详情页
const goToBookDetail = (bookId) => {
  router.push({ name: 'bookDetail', params: { id: bookId } }); // 确保路由已命名为 'bookDetail'
};

// 借阅图书 (列表视图中的按钮)
const borrowBook = (bookId) => {
  // 这里需要调用借阅 API
  console.log(`Attempting to borrow book with ID: ${bookId}`);
  ElMessageBox.confirm('确定要借阅这本书吗？', '借阅确认', {
    confirmButtonText: '确定借阅',
    cancelButtonText: '取消',
    type: 'info',
  }).then(async () => {
    try {
      // 替换为你的实际借阅 API 端点
      // await axios.post(`/api/borrows/`, { book_id: bookId });
      ElMessage.success('借阅成功！(模拟)');
      // 借阅成功后可能需要刷新当前列表或更新该书状态
      const bookIndex = books.value.findIndex(b => b.id === bookId);
      if (bookIndex !== -1) {
          books.value[bookIndex].status = 'borrowed'; // 更新本地状态
      }
      // 或者重新获取当前页数据
      // await fetchBooks(currentPage.value);
    } catch (error) {
      console.error("借阅失败:", error);
      ElMessage.error(error.response?.data?.detail || '借阅失败，请稍后再试');
    }
  }).catch(() => {
    // 用户取消
    ElMessage.info('已取消借阅');
  });
};

// --- Watchers ---
// 监听路由 query 中 search 参数的变化，更新 filterParams.search 并重新获取数据
watch(() => route.query.search, (newSearchQuery) => {
  const currentSearch = newSearchQuery || '';
  if (filterParams.search !== currentSearch) {
    filterParams.search = currentSearch;
    fetchBooks(1); // 搜索词变化，回到第一页
  }
});

// --- Lifecycle Hooks ---
onMounted(async () => {
  await fetchCategories();
  // 页面加载时，根据当前路由参数获取图书
  await fetchBooks(currentPage.value); // 使用 currentPage.value 获取初始页
});
</script>
<style scoped>
.book-list-page {
  /* 页面整体内边距由 app-main 提供 */
}

/* Filter Card Styles */
.filter-card {
  margin-bottom: 20px;
  border: none; /* 去掉卡片边框，更简洁 */
  background-color: #f9fafb; /* 轻微背景色区分 */
}
.filter-form {
  display: flex;
  flex-wrap: wrap; /* 允许换行 */
  gap: 15px; /* 表单项之间的间距 */
  align-items: center;
}
.filter-form .el-form-item {
  margin-bottom: 0; /* 移除 el-form-item 默认的下边距 */
}
/* 让视图切换按钮靠右 */
.filter-form .view-toggle {
    margin-left: auto;
}


/* Books Display Area Styles */
.books-display-area {
  margin-bottom: 20px;
  min-height: 300px; /* 防止加载时区域塌陷 */
}
.book-col {
  margin-bottom: 20px; /* 网格视图卡片下边距 */
}

/* List View Table Styles */
.el-table {
    /* 可以添加一些表格样式 */
}
.el-table .el-button + .el-button {
    margin-left: 8px; /* 调整操作按钮间距 */
}

/* Pagination Styles */
.pagination-container {
  display: flex;
  justify-content: center; /* 居中分页 */
  margin-top: 30px;
}

/* 响应式调整 (可选) */
@media (max-width: 768px) {
  .filter-form {
    flex-direction: column; /* 小屏幕上垂直排列筛选条件 */
    align-items: stretch; /* 拉伸表单项宽度 */
  }
   .filter-form .view-toggle {
      margin-left: 0; /* 取消靠右 */
      margin-top: 10px; /* 添加上边距 */
      align-self: flex-end; /* 按钮组自身靠右 */
   }
}
</style>
