from django.db import migrations

def create_initial_data(apps, schema_editor):
    Category = apps.get_model('books', 'Category')
    Location = apps.get_model('books', 'Location')
    
    # 创建分类
    categories = [
        '文学小说',
        '科学技术',
        '历史传记',
        '艺术设计',
        '经济管理'
    ]
    
    for category_name in categories:
        Category.objects.create(name=category_name)
    
    # 创建位置
    locations = [
        {'name': 'A区-1层', 'description': '一楼A区书架'},
        {'name': 'A区-2层', 'description': '二楼A区书架'},
        {'name': 'B区-1层', 'description': '一楼B区书架'},
        {'name': 'B区-2层', 'description': '二楼B区书架'}
    ]
    
    for loc in locations:
        Location.objects.create(name=loc['name'], description=loc['description'])

def reverse_func(apps, schema_editor):
    Category = apps.get_model('books', 'Category')
    Location = apps.get_model('books', 'Location')
    Category.objects.all().delete()
    Location.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),  # 修改为实际的前一个迁移文件名称
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_func),
    ]