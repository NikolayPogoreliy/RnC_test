from django.db.models import Q
from rest_framework import serializers
from apps.libra.models import Author, Book, Genre


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('url', 'id', 'first_name', 'last_name', 'birth_date', 'sex')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'genre')


class BookSerializer(serializers.HyperlinkedModelSerializer):
    genre = GenreSerializer()
    authors = serializers.SerializerMethodField(read_only=True)
    author = serializers.CharField(write_only=True, source='get_authors')

    def create(self, validated_data):
        authors = validated_data.pop('get_authors')
        genre_name = validated_data.pop('genre').get('genre')
        genre_obj, _ = Genre.objects.get_or_create(genre__iexact=genre_name, defaults={'genre': genre_name})
        book = Book.objects.create(**validated_data, genre=genre_obj)
        book.author.add(*self.__get_authors_objects(authors))
        return book

    def update(self, instance, validated_data):
        print(dict(validated_data))
        authors = validated_data.pop('get_authors')
        genre_name = validated_data.pop('genre').get('genre')
        genre_obj, _ = Genre.objects.get_or_create(genre__iexact=genre_name, defaults={'genre': genre_name})
        instance.genre = genre_obj
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.author.clear()
        instance.author.add(*self.__get_authors_objects(authors))
        return instance

    def get_authors(self, obj):
        return ', '.join([f'{i.first_name} {i.last_name}' for i in obj.author.all()])

    @staticmethod
    def __get_authors_objects(authors):
        authors_obj_list = []
        for author in authors.split(', '):
            author_name = author.split()
            author_obj = Author.objects.filter(
                Q(first_name__iexact=' '.join(author_name[:-1])) |
                Q(first_name__in=author_name[:-1]) |
                Q(first_name__icontains=' '.join(author_name[:-1])),
                last_name__iexact=author_name[-1]
            ).first()
            if author_obj:
                authors_obj_list.append(author_obj)
        return authors_obj_list

    class Meta:
        model = Book
        fields = ('url', 'id', 'title', 'authors', 'author', 'genre', 'publish_date', 'isbn_code')
