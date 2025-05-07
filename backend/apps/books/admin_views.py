from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count
from django.contrib import admin
from .models import Book
import random

@staff_member_required
def dashboard(request):
    book_counts_query = Book.objects.values('category').annotate(count=Count('id')).order_by('category')
    book_categories = [item['category'] for item in book_counts_query]
    book_data_points = [item['count'] for item in book_counts_query]
    active_users_today = random.randint(50, 100)

    context = {
        'book_categories': book_categories,
        'book_data_points': book_data_points,
        'active_users_today': active_users_today,
        'title': '今日数据仪表盘',
        'site_header': getattr(admin.site, 'site_header', 'Django 管理'),
        'site_title': getattr(admin.site, 'site_title', 'Django 站点管理'),
        'has_permission': True,
    }
    return render(request, 'admin/dashboard.html', context)