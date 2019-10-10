from rest_framework import serializers
from apps.libra.models import Author, Book, BookAuthor, Genre


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name', 'birth_date', 'sex')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'genre')


class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthor
        fields = ('id', 'author_id')


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True)
    genre = GenreSerializer()

    def create(self, validated_data):
        authors = validated_data.pop('author')
        genre_name = validated_data.pop('genre').get('genre')
        genre_obj = Genre.objects.filter(genre__iexact=genre_name).first()
        book = Book.objects.create(**validated_data, genre=genre_obj)
        for author in authors:
            author_obj = Author.objects.filter(
                first_name__iexact=author.get('first_name'),
                last_name__iexact=author.get('last_name')
            ).first()
            book.author.add(author_obj)
        return book

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'genre', 'publish_date', 'isbn_code')
