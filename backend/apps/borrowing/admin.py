from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import BorrowingRecord


@admin.register(BorrowingRecord)
class BorrowingRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_title', 'user_name', 'borrow_date', 'due_date', 
                   'return_date', 'is_overdue', 'days_overdue')
    list_filter = ('return_date', 'borrow_date', 'due_date')
    search_fields = ('book__title', 'book__isbn', 'user__name', 'user__student_id')
    date_hierarchy = 'borrow_date'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('借阅信息'), {
            'fields': ('book', 'user', 'borrow_date', 'due_date', 'return_date')
        }),
        (_('系统信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def book_title(self, obj):
        return obj.book.title
    book_title.short_description = _('书名')
    
    def user_name(self, obj):
        return obj.user.name
    user_name.short_description = _('借阅人')
    
    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = _('是否逾期')

# Register your models here.
