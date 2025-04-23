from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = [
            'id', 'username', 'name', 'role', 'department', 'position',
            'student_id', 'email', 'phone', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器"""
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'password', 'confirm_password', 'name', 'role',
            'department', 'position', 'student_id', 'email', 'phone'
        ]
    
    def validate(self, attrs):
        # 验证两次密码是否一致
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "两次密码不一致"})
        
        # 根据角色验证必填字段
        role = attrs.get('role', 'student')
        
        if role == 'student' and not attrs.get('student_id'):
            raise serializers.ValidationError({"student_id": "学生必须提供学号"})
        
        if role == 'admin' and not attrs.get('position'):
            raise serializers.ValidationError({"position": "管理员必须提供职务"})
        
        # 验证密码强度
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        
        return attrs
    
    def create(self, validated_data):
        # 移除确认密码字段
        validated_data.pop('confirm_password')
        
        # 创建用户
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""
    class Meta:
        model = User
        fields = [
            'name', 'department', 'position', 'student_id', 
            'email', 'phone', 'is_active'
        ]
    
    def validate(self, attrs):
        # 获取当前用户角色
        instance = self.instance
        role = instance.role
        
        # 根据角色验证必填字段
        if role == 'student' and 'student_id' in attrs and not attrs['student_id']:
            raise serializers.ValidationError({"student_id": "学生必须提供学号"})
        
        if role == 'admin' and 'position' in attrs and not attrs['position']:
            raise serializers.ValidationError({"position": "管理员必须提供职务"})
        
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        # 验证两次密码是否一致
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"new_password": "两次密码不一致"})
        
        # 验证密码强度
        try:
            validate_password(attrs['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": e.messages})
        
        return attrs