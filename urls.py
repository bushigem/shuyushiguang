from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.books.views import BookViewSet, CategoryViewSet, LocationViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'locations', LocationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]