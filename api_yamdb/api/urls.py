from django.urls import include, path
from rest_framework import routers

from api.views import TitleViewSet, UserViewSet, signup


router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet)
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/', include(router_v1.urls)),
]
