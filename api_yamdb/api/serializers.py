from rest_framework import serializers
from reviews.models import Title
from users.models import User

from api.validators import validate_username


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[validate_username],
    )

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        if User.objects.filter(email=email, username=username).exists():
            return data
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с такми `email` уже существует!')
        elif User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с такми `username` уже существует!')

        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[validate_username]
    )
    confirmation_code = serializers.CharField(max_length=39, required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_field = ('role',)
