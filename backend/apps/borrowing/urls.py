from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BorrowingRecordViewSet

router = DefaultRouter()
router.register('records', BorrowingRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]