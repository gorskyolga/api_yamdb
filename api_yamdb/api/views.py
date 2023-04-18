from rest_framework import viewsets

from api.serializers import TitleSerializer
from titles.models import Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
