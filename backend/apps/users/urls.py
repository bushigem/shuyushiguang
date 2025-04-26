from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
# --- 确保你的视图已正确导入 ---
from .views import UserViewSet, RegistrationView

# --- 用户管理路由 (例如: /api/users/) ---
router = DefaultRouter()
# --- 假设 UserViewSet 用于管理用户，如果暂时没有，可以注释掉或移除 ---
# router.register(r'', UserViewSet, basename='user')

# --- 定义认证相关路由 ---
auth_urlpatterns = [
    path('login/', obtain_auth_token, name='api_token_auth'), # 映射到 /api/auth/login/
    path('register/', RegistrationView.as_view(), name='api_register'), # 映射到 /api/auth/register/
    # 未来可以添加更多认证相关 URL, 如密码重置等
]

# --- 定义用户管理部分的 urlpatterns ---
# --- 如果 router.register 被注释或移除，这里可以为空列表，但变量必须存在 ---
urlpatterns = [
    # path('', include(router.urls)), # 如果 UserViewSet 存在且注册了，取消注释这行
]

# 注意：auth_urlpatterns 会在主项目的 urls.py 中被导入和使用