from django.conf import settings
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from users.models import User


class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'role', 'email')
        model = User


class UserEmailCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=128)
    confirmation_code = serializers.IntegerField(required=True)

    def validate(self, data):
        confirmation_code = data['confirmation_code']
        user = get_object_or_404(User, username=data['username'])
        if confirmation_code == settings.RESET_CONFIRMATION_CODE:
            raise serializers.ValidationError(
                ('Данный код подтверждения уже был использован.'))
        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError('Неверный код подтверждения')
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('Username "me" уже занято.')
        return data
