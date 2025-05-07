INSTALLED_APPS = [
    'django.contrib.admin',
    # 'django.contrib.auth',  # 注释掉认证应用
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'apps.books',  # 添加这行，确保books应用被包含
    'apps.users',  # 如果有users应用也要添加
]

# 在settings.py中添加以下配置，暂时禁用CSRF保护（仅用于测试）
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # 暂时注释掉CSRF中间件
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',  # 注释掉认证中间件
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS设置
CORS_ALLOW_ALL_ORIGINS = True  # 替换原来的 CORS_ALLOWED_ORIGINS
CORS_ALLOW_CREDENTIALS = False
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# 添加额外的 CORS 设置
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# REST Framework 设置
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # 确认是 AllowAny
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [],  # 确认是空列表，移除认证
    # 确保没有其他可能引起冲突的设置，例如 DEFAULT_THROTTLE_CLASSES 等
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles' # 生产环境收集静态文件用

# Media files (User uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' # 确保 'media' 文件夹在项目根目录下存在

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS设置 (保持之前的设置)
# 确保CORS配置正确
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True  # 修改为True，允许携带凭证
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# REST Framework 设置 (保持之前的设置)
# 确保REST框架配置正确
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [],  # 空列表，不使用任何认证
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

# SimpleUI 配置
SIMPLEUI_CONFIG = {
    'system_keep': False,  # 关闭系统菜单
    'menu_display': ['图书管理'],  # 只显示图书管理菜单
    'dynamic': True,  # 开启动态菜单功能
    'menus': [
        {
            'name': '图书管理',
            'icon': 'fas fa-book',
            'models': [
                {
                    'name': '图书列表',
                    'url': '/admin/books/book/',
                    'icon': 'fas fa-list'
                },
                {
                    'name': '分类管理',
                    'url': '/admin/books/category/',
                    'icon': 'fas fa-tags'
                }
            ]
        }
    ]
}

# LOGGING 设置 (保持之前的设置)