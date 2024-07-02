import logging
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from external.paginated_response import CustomPagination
from log_space.models import APILog
from log_space.serializers.serializers_v1 import LogSpaceSerializer
from user_panel.permissions.permission_v1 import IsManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@extend_schema(tags=['log_space'])
class LogSpaceView(viewsets.ReadOnlyModelViewSet):
    model_class = APILog
    queryset = APILog.objects.all()
    serializer_class = LogSpaceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsManager()]
        return [IsAuthenticated(), IsManager()]

    def get_queryset(self):
        logger.info('Fetching APILog queryset.')
        return self.queryset

    def list(self, request, *args, **kwargs):
        logger.info('Listing API logs.')
        response = super().list(request, *args, **kwargs)
        logger.info('Listed API logs successfully.')
        return response

    def retrieve(self, request, *args, **kwargs):
        logger.info(f'Retrieving API log with id {kwargs.get("pk")}.')
        response = super().retrieve(request, *args, **kwargs)
        logger.info(f'API log with id {kwargs.get("pk")} retrieved successfully.')
        return response
