from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from user_panel.models import CustomUser
from user_panel.serializers.serializers_v1 import UserSerializer
from user_panel.permissions.permission_v1 import IsManager, IsCustomer
from rest_framework.exceptions import PermissionDenied


@extend_schema(tags=['User Management'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    method = ['GET', 'POST', 'PUT', 'DELETE']
    lookup_field = 'username'

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve', 'update', 'destroy']:
            return [IsAuthenticated(), IsManager()]
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsCustomer()]
        return [IsAuthenticated(), IsManager()]

    def validate_authentication_token(self, request):
        authentication_token = request.data.get('authentication_token')
        if not authentication_token:
            return Response({'error': 'Authentication token is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.filter(username=request.user, authentication_token=authentication_token).first()
        if not user:
            return Response({'error': 'Invalid authentication token'}, status=status.HTTP_400_BAD_REQUEST)
        return None

    def create(self, request, *args, **kwargs):
        auth_error = self.validate_authentication_token(request)
        if auth_error:
            return auth_error

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
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
        # auth_error = self.validate_authentication_token(request)
        # if auth_error:
        #     return auth_error
        print("Hello List API")
        user_type = request.query_params.get('user_type')
        queryset = self.filter_queryset(self.get_queryset())
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        auth_error = self.validate_authentication_token(request)
        if auth_error:
            return auth_error

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        auth_error = self.validate_authentication_token(request)
        if auth_error:
            return auth_error

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        auth_error = self.validate_authentication_token(request)
        if auth_error:
            return auth_error

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
