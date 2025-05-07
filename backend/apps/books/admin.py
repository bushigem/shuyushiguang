from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from .models import Book, Category, Location
from .forms import BookImportForm
from .admin_views import dashboard # <--- 导入 dashboard 视图

# 先注册分类模型
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    
    # 确保只显示分类相关内容
    def get_queryset(self, request):
        return super().get_queryset(request)

# 再注册位置模型
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    
    # 确保只显示位置相关内容
    def get_queryset(self, request):
        return super().get_queryset(request)

# 最后注册图书模型
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'author', 'publisher', 'status', 'category', 'location', 'added_at')
    list_filter = ('status', 'category', 'location')
    search_fields = ('title', 'isbn', 'author', 'publisher', 'description')
    ordering = ('title',)
    readonly_fields = ('added_at', 'updated_at')
    
    # 添加自定义动作
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-books/', self.admin_site.admin_view(self.import_books), name='import_books'),
        ]
        return custom_urls + urls

    def import_books(self, request):
        if request.method == 'POST':
            form = BookImportForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                self.message_user(request, "批量导入成功")
                return HttpResponseRedirect("../")
        else:
            form = BookImportForm()
        return render(request, 'admin/books/book/import_books.html', {'form': form})

# --- 将 dashboard 视图注册到 admin.site ---
# 获取 Django Admin Site 的默认 get_urls 方法
original_get_urls = admin.site.get_urls

def get_admin_site_urls():
    # 先获取所有默认的 admin URLs
    urls = original_get_urls()
    # 然后添加您的自定义 URL
    # 注意：这里的 path 是相对于 /admin/ 的，所以 'dashboard/' 对应 /admin/dashboard/
    # name='admin_dashboard' 将在 admin 命名空间下，所以完整名称是 admin:admin_dashboard
    custom_urls = [
        path('dashboard/', admin.site.admin_view(dashboard), name='admin_dashboard')
    ]
    return custom_urls + urls

# 使用我们修改后的 get_urls 方法替换掉原来的
admin.site.get_urls = get_admin_site_urls
# --- dashboard 注册结束
