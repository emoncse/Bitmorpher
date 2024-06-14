from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from user_panel.models import CustomUser
from user_panel.serializers.serializers_v1 import UserSerializer
from user_panel.permissions.permission_v1 import IsManager, IsCustomer


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of users",
        responses={200: UserSerializer(many=True)},
    ),
    retrieve=extend_schema(
        description="Retrieve details of a specific user",
        responses={200: UserSerializer},
    ),
    create=extend_schema(
        description="Create a new user",
        request=UserSerializer,
        responses={201: UserSerializer},
    ),
    update=extend_schema(
        description="Update an existing user",
        request=UserSerializer,
        responses={200: UserSerializer},
    ),
    partial_update=extend_schema(
        description="Partially update an existing user",
        request=UserSerializer,
        responses={200: UserSerializer},
    ),
    destroy=extend_schema(
        description="Delete an existing user",
        responses={204: None},
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsManager]
        else:
            permission_classes = [IsAuthenticated, IsCustomer]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'authentication_token': serializer.instance.authentication_token},
                        status=status.HTTP_201_CREATED, headers=headers)
