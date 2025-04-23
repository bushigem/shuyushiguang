from rest_framework import serializers
from .models import Category, Location, Book

class CategorySerializer(serializers.ModelSerializer):
    """书籍分类序列化器"""
    class Meta:
        model = Category
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    """书籍位置序列化器"""
    class Meta:
        model = Location
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    """书籍序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class BookDetailSerializer(serializers.ModelSerializer):
    """书籍详情序列化器"""
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'