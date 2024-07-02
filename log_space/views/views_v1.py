from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from log_space.models import APILog
from log_space.serializers.serializers_v1 import LogSpaceSerializer
from user_panel.permissions.permission_v1 import IsManager


@extend_schema(tags=['log_space'])
class LogSpaceView(viewsets.ReadOnlyModelViewSet):
    model_class = APILog
    queryset = APILog.objects.all()
    serializer_class = LogSpaceSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsManager()]
        return [IsAuthenticated(), IsManager()]

    def get_queryset(self):
        return self.queryset

