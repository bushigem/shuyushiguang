from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate
from .models import User
from .serializers import (
    UserSerializer, 
    UserCreateSerializer, 
    UserUpdateSerializer,
    ChangePasswordSerializer
)
from .permissions import IsSuperAdmin, IsAdminOrSelf # Ensure IsAdminOrSelf is correctly defined
from rest_framework import viewsets, generics, permissions # 添加 generics 和 permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer
)
# 确保导入 AllowAny
from rest_framework.permissions import AllowAny, IsAdminUser
from .permissions import IsSuperAdmin, IsAdminOrSelf


# --- 新增注册视图 ---
class RegistrationView(generics.CreateAPIView):
    """
    用户公共注册视图
    允许任何用户通过 POST 请求创建新用户账户。
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny] # 允许任何人访问此视图进行注册

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 在保存前可以设置默认值，例如角色
        # user = serializer.save(role='student') # 假设默认注册为学生
        user = serializer.save() # 如果 UserCreateSerializer 已经处理了默认值或不需要设置
        headers = self.get_success_headers(serializer.data)
        # 注册成功后不返回 token，用户需要去登录页面登录
        # 可以只返回成功消息或创建的用户信息（不含敏感数据）
        # 为了安全，通常只返回部分信息或仅状态码
        # 这里我们返回创建的用户信息（由 UserCreateSerializer 控制）
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
# --- 注册视图结束 ---


class UserViewSet(viewsets.ModelViewSet):
    """用户视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'department', 'is_active']
    search_fields = ['username', 'name', 'student_id', 'email', 'phone']
    ordering_fields = ['username', 'name', 'created_at']

    def get_permissions(self):
        """根据不同操作设置权限"""
        if self.action == 'create':
            # 只有管理员可以创建用户
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            # 管理员或用户自己可以更新 (具体字段权限在 perform_update 控制)
            permission_classes = [IsAdminOrSelf]
        elif self.action == 'destroy':
             # 管理员或用户自己可以删除 (如果允许用户自删的话)
             # 或者仅限管理员: permission_classes = [IsAdminUser]
            permission_classes = [IsAdminOrSelf] # 或 IsAdminUser
        elif self.action == 'list':
            # 登录用户可以列出用户 (可以考虑改为 IsAdminUser)
            permission_classes = [IsAuthenticated]
        # --- 添加 retrieve 权限 ---
        elif self.action == 'retrieve':
             # 管理员或用户自己可以查看详情
            permission_classes = [IsAdminOrSelf]
        # --- 添加结束 ---
        elif self.action in ['change_password', 'deactivate']:
            # 管理员或用户自己可以修改密码或停用自己
            permission_classes = [IsAdminOrSelf]
        elif self.action == 'activate':
            # 只有管理员可以激活用户
            permission_classes = [IsAdminUser]
        # --- 添加 admins 和 students 动作的权限 ---
        elif self.action in ['admins', 'students']:
             # 假设只有管理员可以查看管理员列表和学生列表
             permission_classes = [IsAdminUser]
        # --- 添加结束 ---
        else:
            # 其他默认操作（如 OPTIONS）允许认证用户
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """根据不同操作返回不同的序列化器"""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer

    # --- 覆盖 perform_update 以控制角色修改权限 ---
    def perform_update(self, serializer):
        """执行更新操作，增加角色修改权限控制"""
        validated_data = serializer.validated_data
        requesting_user = self.request.user

        # 检查是否尝试修改 role 字段
        if 'role' in validated_data:
            # 如果请求者不是管理员，则不允许修改 role
            if not requesting_user.is_staff:
                # 从验证数据中移除 role，防止非管理员修改
                validated_data.pop('role', None)
                # 可选：如果需要，可以在这里记录一个警告或返回特定响应，
                # 但通常静默忽略非权限操作更简单。
                # 注意：此时 is_staff 也不会根据 role 自动更新，因为 role 被移除了

        # 对于管理员，序列化器中的 update 方法会处理 is_staff 的同步
        # 对于非管理员，由于 role 被移除，is_staff 不会改变

        # 调用原始的保存逻辑，但使用可能已修改的 validated_data
        # 注意：这里我们直接调用 serializer.save()，它内部会调用 serializer.update()
        serializer.save()
    # --- 覆盖结束 ---


    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """修改密码"""
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # 验证旧密码
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"old_password": ["旧密码不正确"]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 设置新密码
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"status": "密码已修改"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """激活用户"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"status": "用户已激活"})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """停用用户"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({"status": "用户已停用"})

    @action(detail=False, methods=['get'])
    def students(self, request):
        """获取所有学生"""
        queryset = self.queryset.filter(role='student')
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def admins(self, request):
        """获取所有管理员"""
        queryset = self.queryset.filter(role='admin')
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Create your views here.
