from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from hello.permissions.permissions import IsAuthenticatedOrWriteOnly
from hello.serializers import UserSerializer, ProfileSerializer
from hello.models import Profile


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrWriteOnly,)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permissions_class = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Profile.objects.filter(user__id=self.request.user.id)
