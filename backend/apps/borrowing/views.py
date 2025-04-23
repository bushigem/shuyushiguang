from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q, F, ExpressionWrapper, fields
from django.db.models.functions import Now
from .models import BorrowingRecord
from .serializers import (
    BorrowingRecordSerializer, 
    BorrowingRecordDetailSerializer,
    BorrowBookSerializer,
    ReturnBookSerializer
)


class BorrowingRecordViewSet(viewsets.ModelViewSet):
    """借阅记录视图集"""
    queryset = BorrowingRecord.objects.all()
    serializer_class = BorrowingRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['book', 'user', 'return_date']
    search_fields = ['book__title', 'book__isbn', 'user__name', 'user__student_id']
    ordering_fields = ['borrow_date', 'due_date', 'return_date']

    def get_serializer_class(self):
        """根据不同操作返回不同的序列化器"""
        if self.action == 'retrieve' or self.action == 'list':
            return BorrowingRecordDetailSerializer
        elif self.action == 'borrow':
            return BorrowBookSerializer
        elif self.action == 'return_book':
            return ReturnBookSerializer
        return BorrowingRecordSerializer

    @action(detail=False, methods=['get'])
    def current(self, request):
        """获取当前借阅中的记录"""
        queryset = self.queryset.filter(return_date__isnull=True)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """获取逾期未还的记录"""
        queryset = self.queryset.filter(
            return_date__isnull=True,
            due_date__lt=timezone.now().date()
        )
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def borrow(self, request):
        """借书操作"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """还书操作"""
        instance = self.get_object()
        
        # 检查是否已归还
        if instance.return_date:
            return Response(
                {"detail": "该书籍已归还"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def user_history(self, request):
        """获取用户借阅历史"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {"detail": "必须提供user_id参数"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(user_id=user_id)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def book_history(self, request):
        """获取书籍借阅历史"""
        book_id = request.query_params.get('book_id')
        if not book_id:
            return Response(
                {"detail": "必须提供book_id参数"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(book_id=book_id)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Create your views here.
