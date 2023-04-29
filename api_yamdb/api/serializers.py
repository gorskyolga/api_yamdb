from django.db import transaction
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.validators import validate_username, validate_year
from api_yamdb.settings import (SCORE_MAXVALUE, SCORE_MINVALUE, ErrorMessage,
                                HTTPMethod)
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
    rating = serializers.SerializerMethodField(method_name='get_rating')
    year = serializers.IntegerField(
        min_value=0,
        required=True,
        validators=(validate_year,),
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category',)

    def get_rating(self, obj):
        rating = Review.objects.filter(
            title_id=obj).aggregate(Avg('score'))['score__avg']
        if rating is not None:
            return round(rating, 0)


class TitleCreateUpdateSerializer(TitleSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug', many=True,
                                         queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    @transaction.atomic
    def create(self, validated_data):
        genres = validated_data.pop('genre')
        category = validated_data.pop('category')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            TitleGenre.objects.create(title=title, genre=genre)
        title.category = category
        title.save()
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.category = validated_data.get('category', instance.category)
        genres = validated_data.get('genre', [])
        instance.genre.set(list(genres))
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.SlugRelatedField(read_only=True, slug_field='text')

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='id',
        many=False,
        read_only=True
    )
    score = serializers.IntegerField(
        required=False, min_value=SCORE_MINVALUE, max_value=SCORE_MAXVALUE)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        if self.context['request'].method != HTTPMethod.POST:
            return data
        title = get_object_or_404(
            Title,
            pk=self.context['view'].kwargs.get('title_id')
        )
        author = self.context['request'].user
        if Review.objects.filter(title_id=title, author=author).exists():
            raise serializers.ValidationError(
                ErrorMessage.ALREADY_HAS_REVIEW_ERROR)
        return data


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(validate_username,),
    )

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        if User.objects.filter(email=email, username=username).exists():
            return data
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                ErrorMessage.ALREADY_USED_EMAIL_ERROR)
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                ErrorMessage.ALREADY_USED_USERNAME_ERROR)
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(validate_username,)
    )
    confirmation_code = serializers.CharField(max_length=39, required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_field = ('role',)
