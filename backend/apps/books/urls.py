from django.urls import path, include
from rest_framework.routers import DefaultRouter
# 导入所有需要的视图
from .views import CategoryViewSet, LocationViewSet, BookViewSet, DeepSeekChatView # 确保 DeepSeekChatView 已导入

router = DefaultRouter()
# 注意：将 BookViewSet 注册到 'books' 路径下，而不是根路径，更符合 RESTful 风格
router.register('books', BookViewSet, basename='book')
router.register('categories', CategoryViewSet)
router.register('locations', LocationViewSet)

urlpatterns = [
    # 包含由 router 自动生成的 URL (如 /api/books/, /api/categories/)
    path('', include(router.urls)),
    # 确认这一行存在且正确
    path('chat/', DeepSeekChatView.as_view(), name='deepseek-chat'),
]