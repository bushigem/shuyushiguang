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
    # 确认密码字段，仅用于验证，不存入数据库
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        # 包含前端注册表单会发送的所有字段
        fields = ['id', 'username', 'password', 'confirm_password', 'name', 'student_id', 'email', 'phone', 'department', 'role']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}, 'min_length': 6},
            'role': {'read_only': True} # 角色通常不由用户直接创建时指定，或在此处设置默认值
            # 或者移除 'role'，在 view 的 create 方法中设置默认值
        }

    def validate(self, data):
        """
        验证两次密码是否一致
        """
        if data['password'] != data.pop('confirm_password'): # 使用 pop 移除 confirm_password
            raise serializers.ValidationError({"password": "两次输入的密码不一致。"})
        # 可以在这里添加其他跨字段验证逻辑
        return data

    def create(self, validated_data):
        """
        创建用户并哈希密码，设置默认角色（如果需要）
        """
        # validated_data.pop('confirm_password') # 如果 validate 中没有 pop，在这里 pop
        # 设置默认角色为 'student'
        user = User.objects.create_user(**validated_data, role='student')
        # 或者: user = User.objects.create_user(**validated_data) # 如果模型有默认值
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""
    # --- 添加 role 字段允许更新 ---
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=False)
    # --- 添加结束 ---

    class Meta:
        model = User
        fields = [
            # --- 添加 role 到字段列表 ---
            'name', 'role', 'department', 'position', 'student_id',
            'email', 'phone', 'is_active'
            # --- 添加结束 ---
        ]
        # 可选：如果某些字段只应由管理员更新，可以在视图中根据用户权限选择不同的Serializer

    def validate(self, attrs):
        # 获取当前用户实例，以便知道原始角色
        instance = self.instance
        # 获取请求中尝试设置的角色，如果未提供则使用实例的当前角色
        role = attrs.get('role', instance.role)

        # 根据 *将要成为* 的角色验证必填字段
        # 注意：这里检查的是 attrs 中是否存在该 key，以及其值是否为空
        if role == 'student':
            # 如果尝试将角色改为 student 或保持 student，且 student_id 被设置为空，则报错
            if 'student_id' in attrs and not attrs.get('student_id'):
                 raise serializers.ValidationError({"student_id": "学生角色必须提供学号"})
            # 如果角色是 student，则 position 可以为空，从 attrs 中移除 position (如果存在)
            # 防止非学生用户更新时意外清空 position
            # attrs.pop('position', None) # 或者让模型处理 blank=True, null=True

        elif role == 'admin':
             # 如果尝试将角色改为 admin 或保持 admin，且 position 被设置为空，则报错
             if 'position' in attrs and not attrs.get('position'):
                 raise serializers.ValidationError({"position": "管理员角色必须提供职务"})
             # 如果角色是 admin，则 student_id 可以为空
             # attrs.pop('student_id', None) # 或者让模型处理

        # 其他角色验证...

        return attrs

    # --- 重写 update 方法以处理 is_staff ---
    def update(self, instance, validated_data):
        # 如果 'role' 在验证过的数据中，说明尝试修改角色
        if 'role' in validated_data:
            new_role = validated_data['role']
            # 根据新角色更新 is_staff 状态
            instance.is_staff = (new_role == 'admin')

        # 调用父类的 update 方法来更新其他字段
        return super().update(instance, validated_data)
    # --- 重写结束 ---


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