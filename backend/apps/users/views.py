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
from .permissions import IsSuperAdmin, IsAdminOrSelf


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
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrSelf]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action in ['change_password', 'deactivate']:
            permission_classes = [IsAdminOrSelf]
        elif self.action == 'activate':
            permission_classes = [IsAdminUser]
        else:
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
