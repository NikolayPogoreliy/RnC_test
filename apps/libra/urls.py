from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from apps.libra.views import AuthorViewset, BooksViewset, GenreViewset


router = DefaultRouter()

router.register(r'author', AuthorViewset, basename='author')
router.register(r'genre', GenreViewset)
router.register(r'book', BooksViewset)


urlpatterns = router.urls

author_books_list = AuthorViewset.as_view({'get': 'retrieve'})

urlpatterns += format_suffix_patterns([
    path('author/<int:pk>/<str:books>', author_books_list, name='author-books'),
])
