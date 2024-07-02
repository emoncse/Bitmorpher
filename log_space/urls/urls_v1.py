from django.urls import include, path
from rest_framework.routers import DefaultRouter

from log_space.views.views_v1 import LogSpaceView

router = DefaultRouter()
router.register(r'logs', LogSpaceView, basename='logs')

urlpatterns = [
    path('', include(router.urls)),
]