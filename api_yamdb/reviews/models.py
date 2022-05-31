from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name


class Genre(models.Model):
    genre_name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.genre_name


class Title(models.Model):
    title_name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genres = models.ManyToManyField(Genre, through='TitleGenre')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
        # blank=True,
        # null=True
    )

    def __str__(self):
        return self.title_name


class TitleGenre(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre}{self.title}'



