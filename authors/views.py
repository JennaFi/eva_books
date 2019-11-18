from django.shortcuts import render
from django.http import HttpResponse
from books.models import Author, Book


# Create your views here.
def all_authors(request):
    user = request.user
    authors = Author.objects.all()

    return render(request, 'authors/author_list.html', {'authors': authors})


def one_author(request, slug):
    user = request.user
    author = Author.objects.get(slug=slug)
    books = Book.objects.filter(author=author)

    return render(request, 'authors/one_author.html', {'author': author, 'books': books})

