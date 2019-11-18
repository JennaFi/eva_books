from django.shortcuts import render
from django.http import HttpResponse
from books.models import Book, Author, Review
from itertools import chain


def index(request):

    books = Book.objects.filter(visible=True)

    return render(request, 'home/index.html', {'books': books})


def aboutus(request):

    books = Book.objects.filter(visible=True)

    return render(request, 'home/aboutus.html', {'books': books})


def search(request):

    query = request.GET.get('q')

    authors = Author.objects.filter(name__contains=query)
    books = Book.objects.filter(title__contains=query)
    reviews = Review.objects.filter(title__contains=query)

    search_results = chain(authors, books, reviews)

    return render(request, 'home/search_results.html', {'search_results': search_results})
