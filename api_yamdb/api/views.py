from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from .permissions import AdminModeratAuthorOrReadonly

from django.shortcuts import get_object_or_404

from api.serializers import (TitleSerializer, CommentSerializer, 
                             ReviewSerializer)
from reviews.models import Review, Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AdminModeratAuthorOrReadonly, ]
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        return self.get_title().reviews


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AdminModeratAuthorOrReadonly, ]
    pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_review())

    def get_queryset(self):
        return self.get_review().comments
