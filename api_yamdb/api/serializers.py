from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers


from api.validators import validate_username
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category',)

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        category = validated_data.pop('category')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(**genre)
            TitleGenre.objects.create(title=title, genre=current_genre)
        current_category, status = Category.objects.get_or_create(**category)
        title.category = current_category
        title.save()
        return title

    def get_rating(self, obj):
        rating = Review.objects.filter(
            title_id=obj).aggregate(Avg('score'))['score__avg']
        return round(rating, 0)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.SlugRelatedField(read_only=True, slug_field="text")

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field="id",
        many=False,
        read_only=True
    )

    class Meta:
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = get_object_or_404(
            Title,
            pk=self.context['view'].kwargs.get('title_id')
        )
        author = self.context['request'].user
        if Review.objects.filter(title_id=title, author=author).exists():
            raise serializers.ValidationError(
                "Вы уже оставляли обзор на данное произведение"
            )
        return data


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
