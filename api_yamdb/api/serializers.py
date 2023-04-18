from rest_framework import serializers

from titles.models import Title


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title
