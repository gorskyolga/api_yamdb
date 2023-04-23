from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet, UserViewSet, signup, token


router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='token'),
    path('v1/', include(router_v1.urls)),
]
