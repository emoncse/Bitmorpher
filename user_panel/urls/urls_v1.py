from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user_panel.views.views_v1 import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('get-authentication-token/', UserViewSet.as_view({'get': 'get_authentication_token'}), name='get-authentication-token'),
]

