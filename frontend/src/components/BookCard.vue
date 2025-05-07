<template>
  <el-card :body-style="{ padding: '0px' }" shadow="hover" class="book-card">
    <el-image :src="book.cover || defaultBookCover" class="book-cover" fit="cover" lazy>
       <template #error>
         <div class="image-slot">
           <el-icon><Picture /></el-icon>
         </div>
       </template>
       <template #placeholder>
         <div class="image-slot">Loading...</div>
       </template>
    </el-image>
    <div class="book-info">
      <h4 class="book-title" :title="book.title">{{ book.title }}</h4>
      <p class="book-author" :title="book.author">{{ book.author || '未知作者' }}</p>
      <div class="book-meta" v-if="showRating && book.rating !== undefined">
         <!-- 使用 :model-value 进行单向绑定 -->
         <el-rate
           :model-value="book.rating"
           disabled
           size="small"
           text-color="#ff9900"
           score-template="{value}"
         />
         <span class="rating-score">{{ book.rating?.toFixed(1) }}</span>
      </div>
      <!-- 可以添加其他信息，如出版社、状态等 -->
    </div>
  </el-card>
</template>

<script setup>
import { Picture } from '@element-plus/icons-vue';

// 接收父组件传递的图书信息和配置
defineProps({
  book: {
    type: Object,
    required: true,
    default: () => ({ // 提供默认值以防万一
        title: '未知书名',
        author: '未知作者',
        cover: '',
        rating: 0
    })
  },
  showRating: { // 是否显示评分
      type: Boolean,
      default: false
  }
});

const defaultBookCover = '/default-book-cover.jpg'; // 默认图书封面路径
</script>

<style scoped>
.book-card {
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden; /* Ensure content respects border radius */
}
.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.book-cover {
  width: 100%;
  /* Maintain aspect ratio, e.g., 3:4 */
  aspect-ratio: 3 / 4;
  display: block; /* Remove extra space below image */
}
.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
  font-size: 14px;
}
.image-slot .el-icon {
  font-size: 30px;
}


.book-info {
  padding: 14px;
}

.book-title {
  font-size: 15px;
  font-weight: 500;
  color: #303133;
  margin: 0 0 5px 0;
  /* Ellipsis for long titles */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.book-author {
  font-size: 13px;
  color: #909399;
  margin: 0 0 8px 0;
  /* Ellipsis for long author names */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.book-meta {
    display: flex;
    align-items: center;
    font-size: 12px;
    color: #606266;
}
.rating-score {
    margin-left: 5px;
    color: #ff9900;
    font-weight: bold;
}
</style>