# 图书馆管理系统 (Library Management System)

这是一个基于 Vue.js (前端) 和 Django (后端) 构建的图书馆管理系统项目。

## 功能特性

*   用户认证 (登录/注册 - 假设)
*   图书列表展示 (支持网格/列表视图)
*   图书详情查看
*   图书搜索、筛选 (按分类、状态) 和排序
*   图书分类管理
*   图书位置管理
*   图书批量导入 (Excel)
*   图书批量添加/删除
*   图书借阅/归还 (假设)
*   首页轮播图展示

## 技术栈

*   **前端**:
    *   Vue.js 3 (Composition API, `<script setup>`)
    *   Vue Router
    *   Element Plus UI 库
    *   Axios (HTTP 请求)
    *   Node.js & npm/yarn
*   **后端**:
    *   Python 3
    *   Django 4+
    *   Django REST Framework (DRF)
    *   PostgreSQL / MySQL / SQLite (或其他 Django 支持的数据库)
    *   `django-filter`
    *   `openpyxl`
    *   `django-cors-headers`

## 项目安装与启动

### 先决条件

*   Python (3.8 或更高版本)
*   Node.js (16.x 或更高版本) 和 npm 或 yarn
*   Git
*   数据库 (例如 PostgreSQL, MySQL, 或使用 SQLite)

### 后端启动 (Django)

1.  **克隆仓库** (如果尚未克隆):
    ```bash
    git clone <your-repository-url>
    ```
    ```bash
    cd d:\Project\library\library_management
    ```

2.  **进入后端目录**:
    ```bash
    cd backend
    ```

3.  **创建并激活虚拟环境**:
    ```bash
    python -m venv venv
    ```
    ```bash
    .\venv\Scripts\activate
    ```
    *注意：在不同终端（如 Git Bash）激活命令可能不同 (`source venv/Scripts/activate`)*

4.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **配置数据库**:
    *   打开 `d:\Project\library\library_management\backend\library\settings.py` 文件。
    *   找到 `DATABASES` 配置项。
    *   根据你选择的数据库类型和你的数据库信息 (数据库名, 用户名, 密码, 主机, 端口) 进行修改。
        ```python
        # 例如 PostgreSQL:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'your_db_name',
                'USER': 'your_db_user',
                'PASSWORD': 'your_db_password',
                'HOST': 'localhost', # 或你的数据库主机
                'PORT': '5432',      # 或你的数据库端口
            }
        }
        ```
        ```python
        # 例如 SQLite (默认可能已有):
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
        ```

6.  **配置跨域**:
    *   在 `settings.py` 中，确保 `corsheaders` 在 `INSTALLED_APPS` 中。
    *   确保 `corsheaders.middleware.CorsMiddleware` 在 `MIDDLEWARE` 中 (通常靠近顶部)。
    *   配置允许的源，例如允许来自前端开发服务器的请求：
        ```python
        CORS_ALLOWED_ORIGINS = [
            "http://localhost:8080", # Vue 开发服务器默认端口
            "http://127.0.0.1:8080",
        ]
        # 或者允许所有源 (开发环境):
        # CORS_ALLOW_ALL_ORIGINS = True
        ```

7.  **执行数据库迁移**:
    ```bash
    python manage.py makemigrations
    ```
    ```bash
    python manage.py migrate
    ```

8.  **创建超级用户** (用于访问 Django Admin):
    ```bash
    python manage.py createsuperuser
    ```
    *按照提示输入用户名、邮箱和密码。*

9.  **运行后端开发服务器**:
    ```bash
    python manage.py runserver
    ```
    *默认情况下，后端将在 `http://127.0.0.1:8000/` 运行。*

### 前端启动 (Vue)

1.  **进入前端目录**:
    *   打开一个新的终端窗口。
    ```bash
    cd d:\Project\library\library_management\frontend
    ```

2.  **安装依赖**:
    *   如果你使用 npm:
        ```bash
        npm install
        ```
    *   如果你使用 yarn:
        ```bash
        yarn install
        ```

3.  **配置 API 地址** (如果需要):
    *   检查前端代码中 `axios` 实例的 `baseURL` 或其他 API 请求的地址是否指向正确的后端地址 (例如 `http://localhost:8000`)。
    *   通常可以在 `src/main.js` 或专门的 API 配置文件 (如 `src/api/axios.js`) 中找到。
    *   也可以考虑使用 `.env` 文件来管理环境变量。

4.  **运行前端开发服务器**:
    *   如果你使用 npm:
        ```bash
        npm run serve
        ```
    *   如果你使用 yarn:
        ```bash
        yarn serve
        ```
    *   前端开发服务器通常会运行在 `http://localhost:8080/` (或其他端口，请留意终端输出)。

### 访问应用

*   在浏览器中打开前端开发服务器的地址 (例如 `http://localhost:8080/`) 即可访问图书馆管理系统。
*   可以通过 `http://127.0.0.1:8000/admin/` 访问 Django Admin 后台管理界面 (需要使用之前创建的超级用户登录)。

## API 端点示例

*   `GET /api/books/`: 获取图书列表 (支持分页、过滤、搜索、排序)
*   `POST /api/books/`: 创建新图书
*   `GET /api/books/{id}/`: 获取单本图书详情
*   `PUT /api/books/{id}/`: 更新图书信息
*   `DELETE /api/books/{id}/`: 删除图书
*   `POST /api/books/bulk_add/`: 批量添加图书
*   `DELETE /api/books/bulk_delete/`: 批量删除图书 (需要提供 ID 列表)
*   `POST /api/books/import_books/`: 从 Excel 导入图书
*   `GET /api/books/categories/`: 获取分类列表
*   `GET /api/books/locations/`: 获取位置列表
*   `/api/users/login/` (假设): 用户登录
*   `/api/users/register/` (假设): 用户注册

## 注意事项

*   确保后端和前端服务器都在运行中。
*   如果遇到跨域 (CORS) 问题，请检查后端的 `CORS_ALLOWED_ORIGINS` 或 `CORS_ALLOW_ALL_ORIGINS` 配置。
*   数据库配置需要根据你的实际环境进行调整。