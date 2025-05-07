<template>
  <div class="home-container">
    <!-- <h1>首页测试标题</h1> --> <!-- 移除或注释掉测试标题 -->

    <!-- 取消注释轮播图组件 -->
    <el-card class="carousel-card" shadow="hover">
      <el-carousel :interval="4000" type="card" height="300px">
        <el-carousel-item v-for="(item, index) in carouselItems" :key="index">
          <img :src="item.image" :alt="item.title" class="carousel-image">
          <div class="carousel-caption">
            <h3>{{ item.title }}</h3>
            <p>{{ item.description }}</p>
          </div>
        </el-carousel-item>
      </el-carousel>
    </el-card>
    
    <!-- 热门图书部分 -->
    <h2 class="section-title">热门图书</h2>
    <el-row :gutter="20" class="popular-books-list">
      <el-col :span="6" v-for="book in popularBooks" :key="book.id">
        <el-card shadow="hover" class="book-card">
          <img :src="book.cover || defaultCover" :alt="book.title" class="book-cover">
          <div class="book-info">
            <h4 class="book-title">{{ book.title }}</h4>
            <p class="book-author">{{ book.author }}</p>
            <!-- 可以添加其他信息，如评分、简介等 -->
          </div>
        </el-card>
      </el-col>
    </el-row>
    <!-- ... 其他代码 ... -->
  </div>
</template>

<script setup>
import { ref } from 'vue'; 
// 导入其他需要的组件和函数

// 轮播图数据 (确保图片在 d:\Project\library\library_management\frontend\src\assets\carousel\ 目录下)
const carouselItems = ref([
  {
    title: '新书上架',
    description: '探索我们最新的图书收藏',
    image: require('@/assets/carousel/new-books.jpg') // 检查 new-books.jpg 是否存在
  },
  {
    title: '经典文学',
    description: '品味永恒的文学经典',
    image: require('@/assets/carousel/classics.jpg') // 检查 classics.jpg 是否存在
  },
  {
    title: '科技前沿',
    description: '了解最新科技发展趋势',
    image: require('@/assets/carousel/tech.jpg') // 检查 tech.jpg 是否存在
  },
  {
    title: '读书活动',
    description: '参与我们的读书俱乐部活动',
    image: require('@/assets/carousel/reading-club.jpg') // 检查 reading-club.jpg 是否存在
  }
]);

// 热门图书示例数据
const popularBooks = ref([
  // 使用 require 和 @ 别名引入图片，并使用正斜杠 /
  { id: 1, title: '三体', author: '刘慈欣', cover: require('@/assets/carousel/covers/santi.jpg') }, 
  { id: 2, title: '活着', author: '余华', cover: require('@/assets/carousel/covers/huozhe.jpg') },
  { id: 3, title: '百年孤独', author: '加西亚·马尔克斯', cover: require('@/assets/carousel/covers/bainiangudu.jpg') },
  { id: 4, title: '解忧杂货店', author: '东野圭吾', cover: require('@/assets/carousel/covers/jieyouzahuodian.jpg') },
]);

// 默认封面图片路径 (如果找不到特定封面)
// 确保 d:\Project\library\library_management\frontend\src\assets\images\default-cover.png 文件存在
const defaultCover = require('@/assets/images/default-cover.png'); 

// onMounted(async () => {
//   // 如果有从 API 获取数据的逻辑，可以在这里获取并替换 popularBooks.value
//   // const response = await fetchPopularBooks();
//   // popularBooks.value = response.data;
// });

</script>

<style scoped>
.home-container {
  padding: 20px;
}

/* 轮播图样式 */
.carousel-card {
  margin-bottom: 30px;
  border-radius: 8px;
  overflow: hidden;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.carousel-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 15px;
}

.carousel-caption h3 {
  margin: 0 0 5px 0;
  font-size: 1.5rem;
}

.carousel-caption p {
  margin: 0;
  font-size: 1rem;
}

.popular-books-list {
  margin-top: 20px;
}

.book-card {
  text-align: center;
  margin-bottom: 20px;
}

.book-cover {
  width: 100%;
  max-width: 150px; /* 限制封面最大宽度 */
  height: auto;
  aspect-ratio: 2 / 3; /* 保持常见书籍封面比例 */
  object-fit: cover;
  margin-bottom: 10px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.book-info {
  padding: 0 10px;
}

.book-title {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis; /* 标题过长时显示省略号 */
}

.book-author {
  font-size: 0.9rem;
  color: #666;
}

.section-title {
  margin: 30px 0 20px;
  font-size: 1.8rem;
  color: #333;
  border-left: 4px solid #409EFF;
  padding-left: 15px;
}

/* 其他原有的样式 */
/* ... */
</style>