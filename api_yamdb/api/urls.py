from django.urls import include, path
from rest_framework import DefaultRouter

from .views import ReviewViewSet, CommentViewSet

router = DefaultRouter
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='comments'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/auth/signup/', register, name='register'),
    # path('v1/auth/token/', get_jwt_token, name='token')
]
