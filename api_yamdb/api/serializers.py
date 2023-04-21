from rest_framework import serializers

from django.shortcuts import get_object_or_404

from django.db.models import Avg

from reviews.models import Comment, Review, Title


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        rating = Review.objects.filter(
            title_id=obj).aaggregate(Avg('score'))['score__avg']
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
