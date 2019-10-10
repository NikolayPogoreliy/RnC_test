from rest_framework import viewsets
from apps.libra.models import Author, Book, Genre
from apps.libra.serialisers import AuthorSerializer, GenreSerializer, BookSerializer


class AuthorViewset(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def retrieve(self, request, *args, **kwargs):
        if kwargs.get('books'):
            self.serializer_class = BookSerializer
            self.queryset = Author.objects.get(
                pk=kwargs.get('pk')
            ).author_books.all()

            return super().list(request, *args, **kwargs)
        return super().retrieve(request, *args, **kwargs)


class GenreViewset(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class BooksViewset(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()