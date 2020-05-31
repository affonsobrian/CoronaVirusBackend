from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from api.permissions.permissions import IsAuthenticatedOrWriteOnly, IsAdminOrReadOnly
from api.serializers import (
    UserSerializer,
    ProfileSerializer,
    NotificationTypeSerializer,
    NotificationSerializer,
    AnsweredQuestions,
    QuestionSerializer,
    AnswerQuestionSerializer,
    AnsweredQuestionsSerializer,
    RankSerializerViewSet,
)
from api.models import (
    Profile,
    Notification,
    NotificationType,
    Question,
    AnsweredQuestions,
)
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
    permission_classes = (IsAuthenticated,)
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


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)
    filterset_fields = "__all__"
    ordering_fields = "__all__"

    def get_queryset(self):
        queryset = super(QuestionViewSet, self).get_queryset()
        return queryset.exclude(answeredquestions__user=self.request.user)


class AnswerQuestionsViewSet(viewsets.ModelViewSet):
    queryset = AnsweredQuestions.objects.all()
    serializer_class = AnswerQuestionSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = "__all__"
    ordering_fields = "__all__"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AnsweredQuestionsSerializer
        return AnswerQuestionSerializer


class RankingViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by("-points")
    serializer_class = RankSerializerViewSet
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)
    filterset_fields = "__all__"
    ordering_fields = "__all__"

