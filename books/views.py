from django.shortcuts import render
from .models import Book, User, Author
from .forms import ReviewForm, LoginForm

from django.http import HttpResponse
from datetime import datetime
from .models import Review
from django.contrib.auth import authenticate, login, logout


def all_books(request):

    books = Book.objects.filter(visible=True)

    return render(request, 'books/all_books.html', {'books': books})


def one_book(request, slug):
    book = Book.objects.get(slug=slug)
    reviews = Review.objects.filter(book=book, visible=True)

    form = ReviewForm(request.POST)
    if request.method == 'POST':
        user = request.user
        if not request.user.is_authenticated:
            return HttpResponse('Please log in')

        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']

            new_form = form.save(commit=False)
            new_form.user = request.user
            book = Book.objects.get(slug=slug)
            new_form.book = book

            print('*******', datetime.now(), book)
            new_form.save()

            return render(request, 'home/thankyou.html', {'book': book})

    else:

        form = ReviewForm()

    return render(request, 'books/one_book.html', {'book': book, 'form': form, 'reviews': reviews},

                  )


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('OK')
                else:
                    return HttpResponse('There is no user with that name')
            else:
                return HttpResponse('Password is not correct')
    else:
        form = LoginForm()
    return render(request, 'books/login.html', {'form': form},)

