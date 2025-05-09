from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Location, Book
from .serializers import CategorySerializer, LocationSerializer, BookSerializer, BookDetailSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from .utils import import_books_from_excel
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsAdmin
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Book
from .serializers import BookSerializer
import logging # 添加 logging 导入
from rest_framework import permissions
from openai import OpenAI # 确保导入 OpenAI
import os # 确保导入 os
from rest_framework.views import APIView # 导入 Django settings
from django.conf import settings # 导入 Django settings

# 检查是否有两个 BookViewSet 类定义
# 如果有，需要删除一个，保留下面这个

from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Category, Location
from .serializers import BookSerializer, BookDetailSerializer

# 获取 logger 实例
logger = logging.getLogger(__name__)

# --- 这是我们想要保留的 BookViewSet ---
# 修改BookViewSet类，确保权限设置正确
class BookViewSet(viewsets.ModelViewSet):
    """书籍视图集"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # 确保是AllowAny
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'location']
    search_fields = ['title', 'isbn', 'author', 'publisher', 'description']
    ordering_fields = ['title', 'author', 'publisher', 'publish_date', 'added_at']

    # 只保留一个list方法
    def list(self, request, *args, **kwargs):
        logger.debug(f"进入 BookViewSet list 方法。请求用户: {request.user}")
        logger.debug(f"请求头: {request.headers}")
        logger.debug(f"请求方法: {request.method}")
        logger.debug(f"请求路径: {request.path}")
        try:
            response = super().list(request, *args, **kwargs)
            logger.debug("BookViewSet list 方法成功执行。")
            return response
        except Exception as e:
            logger.error(f"BookViewSet list 方法出错: {e}", exc_info=True)
            raise

    # 覆盖get_permissions方法，确保返回AllowAny
    def get_permissions(self):
        logger.debug("获取权限...")
        perms = [AllowAny()]
        logger.debug(f"返回权限: {[p.__class__.__name__ for p in perms]}")
        return perms
    
    def check_permissions(self, request):
        logger.debug("BookViewSet 开始检查权限...")
        logger.debug(f"请求用户: {request.user}")
        logger.debug(f"请求认证: {request.auth}")
        logger.debug(f"请求方法: {request.method}")
        try:
            super().check_permissions(request)
            logger.debug("BookViewSet 权限检查通过。")
        except Exception as e:
            logger.error(f"BookViewSet 权限检查失败: {e}", exc_info=True)
            raise
    # --- 日志方法结束 ---

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookSerializer

    # --- 保留需要的 action 方法，并根据需要设置权限 ---
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated]) # 导入通常需要登录
    def import_books(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response(
                {'error': '请选择要导入的文件'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            result = import_books_from_excel(file)
            return Response(result)
        except Exception as e:
             logger.error(f"导入书籍失败: {e}", exc_info=True)
             return Response({'error': f'导入失败: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated]) # 批量添加通常需要登录
    def bulk_add(self, request):
        """批量添加书籍"""
        serializer = BookSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated]) # 批量删除通常需要登录
    def bulk_delete(self, request):
        """批量删除书籍"""
        ids = request.data.get('ids', [])
        if not ids:
             return Response({'error': '请提供要删除的书籍ID列表'}, status=status.HTTP_400_BAD_REQUEST)
        count, _ = Book.objects.filter(id__in=ids).delete()
        # 注意：HTTP 204 No Content 不应包含响应体
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- CategoryViewSet 和 LocationViewSet 保持不变 ---
class CategoryViewSet(viewsets.ModelViewSet):
    """书籍分类视图集"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  # 分类也允许匿名访问
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']


class LocationViewSet(viewsets.ModelViewSet):
    """书籍位置视图集"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated] # 位置信息保持需要认证
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']


# --- DeepSeekChatView (确保存在且正确) ---
class DeepSeekChatView(APIView): # 依赖于上面的导入
    """
    处理与 DeepSeek API 的聊天交互
    """
    permission_classes = [AllowAny] # 聊天接口允许匿名访问

    def post(self, request, *args, **kwargs):
        user_message = request.data.get('message')
        if not user_message:
            return Response({"error": "消息不能为空"}, status=status.HTTP_400_BAD_REQUEST)

        # --- 从 Django settings 获取 API Key ---
        api_key = settings.DEEPSEEK_API_KEY # <--- 修改这里，从 settings 读取
        if not api_key: # <--- 检查从 settings 获取的值
             logger.error("DeepSeek API Key 未在 Django settings 或 .env 文件中配置")
             # 返回 500 错误
             return Response({"error": "AI 服务配置错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # --- 获取结束 ---

        try:
            # 使用从 settings 获取的 api_key
            client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个乐于助人的助手。"},
                    {"role": "user", "content": user_message},
                ],
                stream=False
            )

            ai_response = response.choices[0].message.content
            return Response({"reply": ai_response}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"调用 DeepSeek API 时出错: {e}", exc_info=True)
            # 其他异常也会导致 500 错误
            return Response({"error": f"与 AI 服务通信时发生错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --- 确认没有其他重复的 BookViewSet 定义 ---
# (如果之前有注释掉的重复 BookViewSet，请确保它已被删除)
