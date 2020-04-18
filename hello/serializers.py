from django.contrib.auth.models import User, Group
from rest_framework import serializers
from hello.models import Profile

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'first_name', 'last_name', 'username', 'email',
                  'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ("points", "user")

    def validate(self, attrs):
        attrs = super(ProfileSerializer, self).validate(attrs)
        user = self.context['request'].user
        if not user or not user.id:
            raise serializers.ValidationError({"user": "You must be logged to create a profile."})
        search = Profile.objects.filter(user=user)
        if search.exists():
            raise serializers.ValidationError({"user": "A user can have only one profile."})
        attrs['user'] = user
        return attrs

