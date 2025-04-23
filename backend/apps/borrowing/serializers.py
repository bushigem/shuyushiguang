from rest_framework import serializers
from django.utils import timezone
from .models import BorrowingRecord
from apps.books.serializers import BookSerializer
from apps.users.serializers import UserSerializer


class BorrowingRecordSerializer(serializers.ModelSerializer):
    """借阅记录序列化器"""
    days_overdue = serializers.IntegerField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = BorrowingRecord
        fields = '__all__'


class BorrowingRecordDetailSerializer(serializers.ModelSerializer):
    """借阅记录详情序列化器"""
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    days_overdue = serializers.IntegerField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = BorrowingRecord
        fields = '__all__'


class BorrowBookSerializer(serializers.ModelSerializer):
    """借书序列化器"""
    book_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)
    due_date = serializers.DateField(required=True)
    
    class Meta:
        model = BorrowingRecord
        fields = ['book_id', 'user_id', 'due_date']
    
    def validate_due_date(self, value):
        """验证应还日期"""
        if value <= timezone.now().date():
            raise serializers.ValidationError("应还日期必须晚于今天")
        return value
    
    def create(self, validated_data):
        """创建借阅记录"""
        return BorrowingRecord.objects.create(
            book_id=validated_data['book_id'],
            user_id=validated_data['user_id'],
            due_date=validated_data['due_date']
        )


class ReturnBookSerializer(serializers.ModelSerializer):
    """还书序列化器"""
    return_date = serializers.DateField(default=timezone.now().date())
    
    class Meta:
        model = BorrowingRecord
        fields = ['return_date']