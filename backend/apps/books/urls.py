from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, LocationViewSet, BookViewSet

router = DefaultRouter()
router.register('', BookViewSet, basename='book')  # 注册到根路径
router.register('categories', CategoryViewSet)
router.register('locations', LocationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]