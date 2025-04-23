from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from .models import Book, Category, Location
from .forms import BookImportForm

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
