from django.urls import include, path
from rest_framework import routers

from api.views import UserViewSet, GetTokenViewSet, AdminUserViewSet

router = routers.DefaultRouter()
router.register(r'users', AdminUserViewSet, basename='admin_user')

auth_router = routers.DefaultRouter()
auth_router.register(r'signup', UserViewSet, basename='signup')
auth_router.register(r'token', GetTokenViewSet, basename='token')

urlpatterns = [
    path('v1/auth/', include(auth_router.urls)),
    path('v1/', include(router.urls))
]
