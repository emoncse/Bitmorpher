import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from external.paginated_response import CustomPagination
from user_panel.models import CustomUser
from user_panel.serializers.serializers_v1 import UserSerializer
from user_panel.permissions.permission_v1 import IsManager, IsCustomer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@extend_schema(tags=['User Management'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    method = ['GET', 'POST', 'PUT', 'DELETE']
    lookup_field = 'username'
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve', 'update', 'destroy']:
            return [IsAuthenticated(), IsManager()]
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsCustomer()]
        return [IsAuthenticated(), IsManager()]

    def validate_authentication_token(self, request):
        authentication_token = request.data.get('authentication_token')
        if not authentication_token:
            logger.warning('Authentication token is missing in the request.')
            return Response({'error': 'Authentication token is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.filter(username=request.user, authentication_token=authentication_token).first()
        if not user:
            logger.warning('Invalid authentication token provided.')
            return Response({'error': 'Invalid authentication token'}, status=status.HTTP_400_BAD_REQUEST)
        return None

    def create(self, request, *args, **kwargs):
        logger.info('Creating a new user.')
        # auth_error = self.validate_authentication_token(request)
        # if auth_error:
        #     return auth_error

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info(f'User {serializer.data["username"]} created successfully.')
        return Response(
            {'authentication_token': serializer.instance.authentication_token},
            status=status.HTTP_201_CREATED, headers=headers
        )

    @extend_schema(
        description="Retrieve a list of users",
        responses={200: UserSerializer(many=True)},
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'authentication_token': {'type': 'string'},
                },
                'required': ['authentication_token'],
            },
        },
        parameters=[
            OpenApiParameter(name='user_type', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, required=False),
        ],
    )
    def list(self, request, *args, **kwargs):
        logger.info('Listing users.')
        # auth_error = self.validate_authentication_token(request)
        # if auth_error:
        #     return auth_error

        user_type = request.query_params.get('user_type')
        queryset = self.filter_queryset(self.get_queryset())
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f'Retrieved {len(serializer.data)} users.')
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        logger.info('Retrieving user details.')
        # auth_error = self.validate_authentication_token(request)
        # if auth_error:
        #     return auth_error

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        logger.info(f'User {serializer.data["username"]} details retrieved successfully.')
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info('Updating user details.')
        auth_error = self.validate_authentication_token(request)
        if auth_error:
            return auth_error

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info(f'User {serializer.data["username"]} updated successfully.')
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info('Deleting user.')
        auth_error = self.validate_authentication_token(request)
        if auth_error:
            return auth_error

        instance = self.get_object()
        self.perform_destroy(instance)
        logger.info(f'User {instance.username} deleted successfully.')
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_authentication_token(self, request, *args, **kwargs):
        logger.info('Retrieving authentication token for user.')
        authentication_token = CustomUser.objects.get(username=request.user).authentication_token
        logger.info(f'Authentication token retrieved successfully for user {request.user}.')
        return Response({'authentication_token': authentication_token})
