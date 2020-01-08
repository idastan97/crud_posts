from django.urls import path, include
from .views import Register, CheckToken, login, PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', login),
    path('auth/register/', Register.as_view()),
    path('auth/checktoken/', CheckToken.as_view()),
]
