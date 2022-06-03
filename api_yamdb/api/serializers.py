from review.models import Genre, Category, Title, TitleGenre
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
import datetime


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category
        lookup_field = 'slug'


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        required=True,
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genres = serializers.SlugRelatedField(
        required=True,
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = (
            'id',
            'genres',
            'title_name',
            'description',
            'year',
            'category',
        )
        model = Title

    def validate_year(self, value):
        year = datetime.datetime.now().year
        if not (value <= year):
            raise serializers.ValidationError('Year cant be more current year')
        return value


class TitleGetSerializer(serializers.ModelSerializer):
    """rating, пока отсутствует модель review, просто показывает год через метод.
    При получении модели review строку methodfield и метод get_rating
    удалить"""
    category = CategorySerializer(required=True)
    genres = GenreSerializer(many=True, required=True)
    rating = serializers.SerializerMethodField()
    # rating = serializers.IntegerField(source='review.score', read_only=True)
    class Meta:
        fields = (
            'id',
            'genres',
            'title_name',
            'description',
            'year',
            'category',
            'rating'
        )
        model = Title

    def get_rating(self, obj):
        return obj.year


