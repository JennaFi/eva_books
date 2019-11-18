from django.contrib import admin
from books.models import Author, Book, Review, AuthorAdmin, BookAdmin, ReviewAdmin

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)


admin.site.site_header = 'Eva`s Books ADMIN'

# Register your models here.
