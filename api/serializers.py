from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import (
    Profile,
    Notification,
    NotificationType,
    Answer,
    AnsweredQuestions,
    Question,
)
from api.constants.business import POINTS_PER_QUESTION
from django.http import JsonResponse

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "first_name", "last_name", "username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ("points", "user")

    def validate(self, attrs):
        attrs = super(ProfileSerializer, self).validate(attrs)
        # Get Attributes
        x = attrs.get("coordinate_x", None)
        y = attrs.get("coordinate_y", None)
        address = attrs.get("address", None)
        user = self.context["request"].user

        # Check if the user sent a location
        if not (x or y) and not address:
            raise serializers.ValidationError(
                {"address": "You must pass X and Y positions or the address"}
            )

        # Check if user has a profile already
        search = Profile.objects.filter(user=user)
        if search.exists():
            raise serializers.ValidationError(
                {"user": "A user can have only one profile."}
            )

        # Insert user in the attributes
        attrs["user"] = user
        return attrs


class NotificationTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NotificationType
        fields = "__all__"


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class AnswerIdDescriptionOnlySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True, write_only=True)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "description", "is_correct")


class AnswerQuestionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "description")


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerQuestionViewSerializer(many=True, read_only=True)
    is_answered = serializers.SerializerMethodField()

    def get_is_answered(self, obj):
        user = self.context["request"].user
        if user and user.id:
            return AnsweredQuestions.objects.filter(question=obj, user=user).exists()
        return False

    class Meta:
        model = Question
        fields = ("url", "title", "description", "answers", "is_answered")


class AnsweredQuestionsSerializer(serializers.HyperlinkedModelSerializer):
    correct_answers = serializers.SerializerMethodField()

    def get_correct_answers(self, obj):
        answers = obj.question.answers.filter(is_correct=True)
        serializer = AnswerSerializer(answers, many=True)
        return serializer.data

    class Meta:
        model = AnsweredQuestions
        fields = ("url", "question", "correct_answers")


class AnswerQuestionSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerIdDescriptionOnlySerializer(many=True, write_only=True)

    class Meta:
        model = AnsweredQuestions
        fields = ("url", "question", "answers")

    def validate(self, attrs):
        # Calls super validate method
        attrs = super(AnswerQuestionSerializer, self).validate(attrs)
        # Get info
        user = self.context["request"].user
        question = attrs.get("question")

        # Validate if it was not answered already
        is_answered = AnsweredQuestions.objects.filter(
            user=user, question=question
        ).exists()
        if is_answered:
            raise serializers.ValidationError(
                {"user": "You already answered this questions!"}
            )
        return attrs

    def create(self, validated_data):
        # Get information
        question = validated_data.get("question")
        answers = validated_data.get("answers")
        user = self.context["request"].user

        # Get answers ids
        answers = [list(a.values())[0] for a in answers]

        # Check if it is correct
        correctAnswers = question.answers.filter(is_correct=True).values_list(
            "id", flat=True
        )

        is_correct = set(answers) == set(correctAnswers)

        # Give points
        if is_correct:
            user.profile.points += POINTS_PER_QUESTION

        # Save in the database
        instance = AnsweredQuestions.objects.create(
            user=user, question=question, is_correct=is_correct
        )
        user.profile.save()
        return instance


class RankSerializerViewSet(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Profile
        fields = ("user", "points")
        read_only_fields = ("user", "points")

