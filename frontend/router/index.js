import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import BookList from '../views/BookList.vue';
import PersonalCenter from '../views/PersonalCenter.vue';

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/booklist', name: 'booklist', component: BookList },
  { path: '/personalcenter', name: 'personalcenter', component: PersonalCenter },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;