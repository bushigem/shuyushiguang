"""
URL configuration for library project.
"""
from django.contrib import admin
from django.urls import path, include # 确保 include 已导入
from django.conf import settings
from django.conf.urls.static import static
# --- 从 users 应用导入分离出的认证 URL ---
from apps.users.urls import auth_urlpatterns as users_auth_urls
from apps.books.admin_views import dashboard # 确保正确导入 dashboard 视图

urlpatterns = [
    path('admin/', admin.site.urls), # Django Admin 的主路由应该保留
    path('admin/dashboard/', dashboard, name='admin-dashboard'), # 确保 dashboard 路由存在
    # --- 用户管理 URL (如果 UserViewSet 存在且用于此目的) ---
    path('api/users/', include('apps.users.urls')), # 这将包含 UserViewSet 的路由，前缀为 /api/users/
    # --- 认证 URL ---
    path('api/auth/', include(users_auth_urls)), # 包含登录、注册等，前缀为 /api/auth/
    # --- 其他应用的 URL ---
    path('api/books/', include('apps.books.urls')),
    path('api/borrowing/', include('apps.borrowing.urls')),
    path('api-auth/', include('rest_framework.urls')), # DRF 自带的登录/注销（用于 Browsable API）
    path('admin/dashboard/', dashboard, name='admin-dashboard'),
    # ... existing code ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
