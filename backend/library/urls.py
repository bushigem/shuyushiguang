"""
URL configuration for library project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# --- 从 users 应用导入分离出的认证 URL ---
from apps.users.urls import auth_urlpatterns as users_auth_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    # --- 用户管理 URL (如果 UserViewSet 存在且用于此目的) ---
    path('api/users/', include('apps.users.urls')), # 这将包含 UserViewSet 的路由，前缀为 /api/users/
    # --- 认证 URL ---
    path('api/auth/', include(users_auth_urls)), # 包含登录、注册等，前缀为 /api/auth/
    # --- 其他应用的 URL ---
    path('api/books/', include('apps.books.urls')),
    path('api/borrowing/', include('apps.borrowing.urls')),
    path('api-auth/', include('rest_framework.urls')), # DRF 自带的登录/注销（用于 Browsable API）
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
