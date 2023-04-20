from django.urls import include, path
from rest_framework import routers

from api.views import TitleViewSet


router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
