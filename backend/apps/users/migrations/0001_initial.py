# Generated by Django 4.2.20 on 2025-04-20 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='用户名')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('role', models.CharField(choices=[('super_admin', '超级管理员'), ('admin', '管理员'), ('student', '学生')], default='student', max_length=20, verbose_name='角色')),
                ('department', models.CharField(blank=True, max_length=100, verbose_name='院系')),
                ('position', models.CharField(blank=True, max_length=100, verbose_name='职务')),
                ('student_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='学号')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, unique=True, verbose_name='邮箱')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='电话')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否激活')),
                ('is_staff', models.BooleanField(default=False, verbose_name='是否为员工')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'users',
            },
        ),
    ]
