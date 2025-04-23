from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    """书籍分类模型"""
    name = models.CharField(max_length=100, unique=True, verbose_name=_('分类名称'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('创建时间'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('更新时间'))

    class Meta:
        verbose_name = _('书籍分类')
        verbose_name_plural = verbose_name
        db_table = 'categories'

    def __str__(self):
        return self.name


class Location(models.Model):
    """书籍存放位置模型"""
    name = models.CharField(max_length=100, unique=True, verbose_name=_('位置名称'))
    description = models.TextField(blank=True, null=True, verbose_name=_('位置描述'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('创建时间'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('更新时间'))

    class Meta:
        verbose_name = _('存放位置')
        verbose_name_plural = verbose_name
        db_table = 'locations'

    def __str__(self):
        return self.name


class Book(models.Model):
    """书籍信息模型"""
    STATUS_CHOICES = [
        ('available', _('可借')),
        ('borrowed', _('已借出')),
        ('lost', _('丢失')),
        ('damaged', _('损坏')),
        ('reserved', _('已预约')),
    ]

    title = models.CharField(max_length=255, verbose_name=_('书名'))
    isbn = models.CharField(max_length=20, unique=True, verbose_name=_('ISBN号'))
    author = models.CharField(max_length=255, blank=True, verbose_name=_('作者'))
    publisher = models.CharField(max_length=255, blank=True, verbose_name=_('出版社'))
    publish_date = models.DateField(null=True, blank=True, verbose_name=_('出版日期'))
    description = models.TextField(blank=True, verbose_name=_('简介'))
    image_url = models.CharField(max_length=512, blank=True, verbose_name=_('封面图片URL'))
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='books',
        verbose_name=_('所属分类')
    )
    
    location = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='books',
        verbose_name=_('存放位置')
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name=_('状态')
    )
    
    added_at = models.DateTimeField(auto_now_add=True, verbose_name=_('入库时间'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('更新时间'))

    class Meta:
        verbose_name = _('图书')
        verbose_name_plural = verbose_name
        db_table = 'books'

    def __str__(self):
        return f"{self.title} ({self.isbn})"

# Create your models here.
