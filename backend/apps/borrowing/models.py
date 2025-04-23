from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.books.models import Book
from apps.users.models import User


class BorrowingRecord(models.Model):
    """借阅记录模型"""
    book = models.ForeignKey(
        Book, 
        on_delete=models.RESTRICT,
        related_name='borrowing_records',
        verbose_name=_('借阅书籍')
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.RESTRICT,
        related_name='borrowing_records',
        verbose_name=_('借阅用户')
    )
    borrow_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('借出日期')
    )
    due_date = models.DateField(
        verbose_name=_('应还日期')
    )
    return_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name=_('实际归还日期')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('创建时间')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('更新时间')
    )

    class Meta:
        verbose_name = _('借阅记录')
        verbose_name_plural = verbose_name
        db_table = 'borrowing_records'
        ordering = ['-borrow_date']

    def __str__(self):
        return f"{self.user.name} 借阅 {self.book.title} ({self.borrow_date.strftime('%Y-%m-%d')})"

    def clean(self):
        """验证借阅记录的有效性"""
        # 检查书籍是否可借
        if self.book.status != 'available' and not self.pk:
            raise ValidationError(_('该书籍当前不可借阅'))
        
        # 检查归还日期是否合理
        if self.return_date and self.return_date < self.borrow_date.date():
            raise ValidationError(_('归还日期不能早于借出日期'))
        
        # 检查应还日期是否合理
        if self.due_date < self.borrow_date.date():
            raise ValidationError(_('应还日期不能早于借出日期'))

    def save(self, *args, **kwargs):
        """重写保存方法，自动更新书籍状态"""
        is_new = self.pk is None
        
        # 如果是新记录，将书籍状态改为已借出
        if is_new:
            self.book.status = 'borrowed'
            self.book.save()
        
        # 如果设置了归还日期，将书籍状态改为可借
        elif self.return_date and not self.return_date_changed():
            self.book.status = 'available'
            self.book.save()
        
        super().save(*args, **kwargs)
    
    def return_date_changed(self):
        """检查归还日期是否被修改"""
        if not self.pk:
            return False
        
        old_record = BorrowingRecord.objects.get(pk=self.pk)
        return old_record.return_date != self.return_date
    
    @property
    def is_overdue(self):
        """检查是否逾期"""
        if self.return_date:
            return self.return_date > self.due_date
        return timezone.now().date() > self.due_date
    
    @property
    def days_overdue(self):
        """计算逾期天数"""
        if not self.is_overdue:
            return 0
        
        if self.return_date:
            return (self.return_date - self.due_date).days
        
        return (timezone.now().date() - self.due_date).days
# Create your models here.
