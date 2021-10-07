from datetime import date
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'


class Humon(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    age = models.PositiveIntegerField(verbose_name='Возраст', default=0)
    description = models.TextField(verbose_name='о нем')
    image = models.ImageField(upload_to='actors/', verbose_name='изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актёр'
        verbose_name_plural = 'Актeры'


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    tagline = models.CharField(verbose_name='Слоган', max_length=255, default='')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='постер', upload_to='movies/')
    year = models.PositiveSmallIntegerField(verbose_name='Дата выхода', default=2021)
    country = models.CharField(verbose_name='Страна', max_length=200)
    directors = models.ManyToManyField(Humon, verbose_name='Режисер', related_name='film_director')
    actors = models.ManyToManyField(Humon, verbose_name='Актер')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    world = models.DateField(verbose_name='Примьера в мире', default=date.today)
    budjet = models.PositiveIntegerField(verbose_name='Бюджет', default=0, help_text='укажите сумму в Долларах')
    fees_in_usa = models.PositiveIntegerField(verbose_name='Сборы в США', default=0, help_text='СЧборы в США')
    fees_in_world = models.PositiveIntegerField(verbose_name='Сборы в США', default=0, help_text='СЧборы в мире')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=100, unique=True)
    draft = models.BooleanField(verbose_name='Черновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews.set.filter(parent_isnull=True)


class MovieShots(models.Model):
    title = models.CharField(verbose_name='Название', max_length=50)
    description = models.TextField(verbose_name='Описание')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Стоп кадр', upload_to='movies/shots/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадры из фильма'
        verbose_name = 'Кадры из фильмов'


class Ratingstar(models.Model):
    volue = models.SmallIntegerField(verbose_name='значение', default=0)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return self.volue

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name = 'Звёзды рейтингов'


class Review(models.Model):
    email = models.EmailField(verbose_name='почта')
    name = models.CharField(max_length=255, verbose_name='Имя')
    text = models.TextField(blank=True, verbose_name='Отзывы')
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='children')
    movie = models.ForeignKey('Movie', verbose_name='Фильм', on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'{self.name}={self.movie}'

    class Meta:
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'
