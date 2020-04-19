from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from api.permissions.permissions import IsAuthenticatedOrWriteOnly, IsAdminOrReadOnly
from api.serializers import UserSerializer, ProfileSerializer, NotificationTypeSerializer, NotificationSerializer
from api.models import Profile, Notification, NotificationType
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrWriteOnly,)
    filterset_fields = "__all__"
    ordering_fields = "__all__"

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permissions_class = (IsAuthenticatedOrReadOnly,)
    filterset_fields = "__all__"
    ordering_fields = "__all__"

    def get_queryset(self):
        return Profile.objects.filter(user__id=self.request.user.id)

class NotificationTypeViewSet(viewsets.ModelViewSet):
    queryset = NotificationType.objects.all()
    serializer_class = NotificationTypeSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_fields = "__all__"
    ordering_fields = "__all__"

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_fields = "__all__"
    ordering_fields = "__all__"