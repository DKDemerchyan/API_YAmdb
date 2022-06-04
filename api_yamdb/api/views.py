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
from api.permissions import IsAdminOrSuperUser
from users.models import User


class AdminUserViewSet(viewsets.ModelViewSet):
    """API for admin actions: get, post, patch, delete users info.
    """
    queryset = User.objects.all()
    serializer_class = FullUserSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    permission_classes = (IsAdminOrSuperUser,)
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
