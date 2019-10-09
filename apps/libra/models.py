from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


def current_year():
    return timezone.datetime.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Author(models.Model):
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150)
    birth_date = models.DateField(verbose_name='Date of Birth')
    sex = models.NullBooleanField(choices=((None, ''), (True, 'Female'), (False, 'Male')))

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return f'{"".join(map(lambda x: f"{x[0]}.", self.first_name.split()))} {self.last_name}'

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(to=Author, related_name='author_books')
    genre = models.ForeignKey('Genre', related_name='genre_books', on_delete=models.SET('unknown'))
    publish_date = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(400), max_value_current_year),
        default=current_year(),
        null=True
    )
    isbn_code = models.CharField(max_length=25, null=True, unique=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    genre = models.CharField(max_length=80)

    def __str__(self):
        return self.genre
