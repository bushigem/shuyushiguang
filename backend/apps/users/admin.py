from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'name', 'role', 'department', 'student_id', 
                   'email', 'phone', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'department')
    search_fields = ('username', 'name', 'student_id', 'email', 'phone')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('个人信息'), {'fields': ('name', 'email', 'phone')}),
        (_('角色信息'), {'fields': ('role', 'department', 'position', 'student_id')}),
        (_('权限'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('重要日期'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'name', 'role'),
        }),
    )

# Register your models here.
