from reviews.models import Genre, Category, Title, TitleGenre
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    # categories = serializers.StringRelatedField(read_only=True)
    genres = GenreSerializer(many=True,)

    class Meta:
        fields = '__all__'
        model = Title

    def create(self, validated_data):
        if 'genres' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        genres = validated_data.pop('genres')
        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(**genre)
            TitleGenre.objects.create(genre=current_genre, title=title)
            return title



