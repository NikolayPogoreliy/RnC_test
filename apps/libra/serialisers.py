from django.db.models import Q
from rest_framework import serializers
from apps.libra.models import Author, Book, BookAuthor, Genre


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('url', 'id', 'first_name', 'last_name', 'birth_date', 'sex')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'genre')


class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name')


class BookSerializer(serializers.HyperlinkedModelSerializer):
    # author = BookAuthorSerializer(many=True)
    genre = GenreSerializer()
    authors = serializers.SerializerMethodField(read_only=True)
    author = serializers.CharField()

    def create(self, validated_data):
        authors = validated_data.pop('author')
        genre_name = validated_data.pop('genre').get('genre')
        genre_obj = Genre.objects.filter(genre__iexact=genre_name).first()
        book = Book.objects.create(**validated_data, genre=genre_obj)
        for author in authors.split(', '):
            author_name = author.split()
            author_obj = Author.objects.filter(
                Q(first_name__iexact=' '.join(author_name[:-1])) |
                Q(first_name__in=author_name[:-1]) |
                Q(first_name__icontains=' '.join(author_name[:-1])),
                last_name__iexact=author_name[-1]
            ).first()
            book.author.add(author_obj)
        return book

    def get_authors(self, obj):
        return ', '.join([f'{i.first_name} {i.last_name}' for i in obj.author.all()])

    class Meta:
        model = Book
        fields = ('url', 'id', 'title', 'authors', 'author', 'genre', 'publish_date', 'isbn_code')
