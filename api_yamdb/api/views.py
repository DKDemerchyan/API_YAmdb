from review.models import Genre, Category, Title
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CategorySerializer, GenreSerializer, TitleGetSerializer, TitlePostSerializer
from .permissions import IsSuperUserOrReadOnly
from .pagination import ItemPagination
from .filter import TitlesFilter


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    pagination_class = ItemPagination
    serializer_class = GenreSerializer
    permission_classes = (IsSuperUserOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('genre_name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    pagination_class = ItemPagination
    serializer_class = CategorySerializer
    # permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category_name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = ItemPagination
    # permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('title_name', 'year')
    filter_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitlePostSerializer
