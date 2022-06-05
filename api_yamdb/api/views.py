from review.models import Genre, Category, Title
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CategorySerializer, GenreSerializer, TitleGetSerializer, TitlePostSerializer
# from .permissions import IsSuperUserOrReadOnly
# from .pagination import ItemPagination
from rest_framework.pagination import LimitOffsetPagination
from .filter import TitlesFilter
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import (
    mixins, status, viewsets, filters, pagination, permissions
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action

from api.serializers import (
    UserSerializer, UserEmailCodeSerializer, FullUserSerializer
)
from .utils import send_email, code_gen
from api.permissions import IsAdminOrSuperUser, IsAdminOrReadOnly
from users.models import User
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .serializers import CommentSerializer, ReviewSerializer
from review.models import Title, Comment, Review


class AdminUserViewSet(viewsets.ModelViewSet):
    """API for admin actions: get, post, patch, delete users info.
    """
    queryset = User.objects.all()
    serializer_class = FullUserSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    permission_classes = (IsAdminOrSuperUser, IsAuthenticated)
    pagination_class = pagination.LimitOffsetPagination
    search_fields = ('username',)

    @action(detail=False, url_path='me', methods=['GET', 'PATCH'],
            permission_classes=(permissions.IsAuthenticated,))
    def user_get_patch_page(self, request):
        """
        Add "me" page for authenticated user: /users/me

        Returns:
            Response object

        """
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(role=user.role, partial=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_200_OK, headers=headers)

    def perform_create(self, serializer):
        code = code_gen()
        send_email(serializer.validated_data.get('email'), code)
        serializer.save(confirmation_code=code)


class GetTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """API for generating token response.
    """
    queryset = User.objects.all()
    serializer_class = UserEmailCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        user = get_object_or_404(
            User, username=serializer.data.get('username')
        )
        user.confirmation_code = settings.RESET_CONFIRMATION_CODE
        user.save()
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)}, status=status.HTTP_200_OK, headers=headers)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly,]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminOrReadOnly,]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category', 'genres')
    # filter_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitlePostSerializer
>>>>>>> origin/General


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    #  permission_classes = [IsAdminModeratorAuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    #  permission_classes = [IsAdminModeratorAuthorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Comment, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)

        serializer.save(author=self.request.user, review=review)
