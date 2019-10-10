from django.contrib import admin
from apps.libra.models import Author, Book, BookAuthor, Genre

# Register your models here.

admin.site.register(Author)
admin.site.register(Genre)


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1


class BookAdmin(admin.ModelAdmin):
    inlines = (BookAuthorInline,)


admin.site.register(Book, BookAdmin)