from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BorrowingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.borrowing'
    verbose_name = _('借阅管理')
