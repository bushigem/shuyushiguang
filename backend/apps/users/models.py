from django.db import models
# 确保导入 Group 和 Permission
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
    """自定义用户管理器"""
    def create_user(self, username, name, password=None, **extra_fields):
        if not username:
            raise ValueError(_('用户名不能为空'))
        if not name:
            raise ValueError(_('姓名不能为空'))
        
        user = self.model(
            username=username,
            name=name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, name, password=None, **extra_fields):
        extra_fields.setdefault('role', 'super_admin')
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('role') != 'super_admin':
            raise ValueError(_('超级管理员必须具有 super_admin 角色'))
        
        return self.create_user(username, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """用户模型"""
    ROLE_CHOICES = [
        ('super_admin', _('超级管理员')),
        ('admin', _('管理员')),
        ('student', _('学生')),
    ]
    
    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('用户名')
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('姓名')
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name=_('角色')
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('院系')
    )
    position = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('职务')
    )
    student_id = models.CharField(
        max_length=50,
        blank=True,
        unique=True,
        null=True,
        verbose_name=_('学号')
    )
    email = models.EmailField(
        max_length=100,
        blank=True,
        unique=True,
        null=True,
        verbose_name=_('邮箱')
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('电话')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('是否激活')
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('是否为员工')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('创建时间')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('更新时间')
    )

    # --- 添加以下字段定义以解决 related_name 冲突 ---
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        # 指定唯一的 related_name
        related_name="library_user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        # 指定唯一的 related_name
        related_name="library_user_permissions",
        related_query_name="user",
    )
    # --- 添加结束 ---

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = verbose_name
        db_table = 'users'
    
    def __str__(self):
        return f"{self.name} ({self.username})"
    
    def clean(self):
        """验证用户数据的有效性"""
        super().clean()
        
        # 学生必须有学号
        if self.role == 'student' and not self.student_id:
            from django.core.exceptions import ValidationError
            raise ValidationError(_('学生必须提供学号'))
        
        # 管理员必须有职务
        if self.role == 'admin' and not self.position:
            from django.core.exceptions import ValidationError
            raise ValidationError(_('管理员必须提供职务'))
    
    @property
    def is_admin(self):
        return self.role in ['admin', 'super_admin']
    
    @property
    def is_student(self):
        return self.role == 'student'
# Create your models here.
