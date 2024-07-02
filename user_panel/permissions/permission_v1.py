from rest_framework.permissions import BasePermission

from user_panel.models import CustomUser


class IsManager(BasePermission):
    queryset = CustomUser.objects.all()

    def get_queryset(self):
        return self.queryset

    def has_permission(self, request, view):
        queryset = self.get_queryset().filter(username=request.user, user_type='manager').first()
        if queryset:
            return True
        return False


class IsCustomer(BasePermission):
    queryset = CustomUser.objects.all()

    def get_queryset(self):
        return self.queryset

    def has_permission(self, request, view):
        queryset = self.get_queryset().filter(username=request.user, user_type='customer').first()
        if queryset:
            return True
        return False
