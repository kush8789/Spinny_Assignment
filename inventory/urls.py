from django.urls import path, include
from rest_framework import routers
from .views import BoxViewSet


router = routers.DefaultRouter()
router.register(r'boxes', BoxViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]