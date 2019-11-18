from django.db import models
from django.contrib.auth import settings
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from django.contrib import admin

from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget
from django.urls import reverse




User = get_user_model()


class AdminImageWidget(AdminFileWidget):

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(u' <a href="%s" target="_blank"><img src="%s" alt="%s" width="100" style "object-fit: cover;"/></a> %s ' % \
                          (image_url, image_url, file_name, ('')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class Author(models.Model):
    name = models.CharField(max_length=200)
    second_name = models.CharField(max_length=200)
    image = models.FileField(upload_to='author_imgs/', blank=True)
    about = HTMLField(default="About author")
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    books = models.CharField(max_length=200000, blank=True, null=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def __str__(self):
        return str(' '+ self.name+' '+ self.second_name)

    class Meta:
        verbose_name_plural = 'Authors'
        verbose_name = 'Author'
        index_together = ('id', 'slug',)

    def get_absolute_url(self):
        return reverse('authors: author-detail', args=[self.slug, self.id])


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    year = models.CharField(max_length=4)
    rating = models.IntegerField(default=0)
    my_review = HTMLField(default="My review")
    image = models.FileField(upload_to='book_imgs/', blank=True)
    #related_books = models.CharField()
    visible = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    @mark_safe
    def small_img(self):
        return f'<img src="{self.image.url}" height="200";/>' if self.image else ''
    small_img.short_description = "Image"
    small_img.allow_tags = True

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = 'Books'
        verbose_name = 'Book'
        index_together = ('id', 'slug',)

    def get_absolute_url(self):
        return reverse('book: book',
                       args=[self.title, self.image, self.rating, self.my_review, self.author, self.id])


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'small_img',)
    list_filter = ('author', 'rating',)
    fields = ('title', 'author', 'year', 'rating', 'my_review', 'image', 'visible', 'slug')
    list_display_links = ('title', 'author',)
    prepopulated_fields = {'slug': ('title',)}

    #readonly_fields = ('small_img',)


class BookInLine(admin.TabularInline):
    model = Book
    formfield_overrides = {models.FileField: {'widget': AdminImageWidget}}
    fields = ('title', 'year', 'image', 'slug')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'second_name', 'slug')
    list_filter = ('second_name',)
    fields = ('name', 'second_name', 'books', 'slug', 'about', 'image', 'date_of_birth', 'date_of_death')
    list_display_links = ('name', 'second_name', 'slug')
    inlines = [BookInLine,
               ]
    prepopulated_fields = {'slug': ('name', 'second_name',)}


class Review(models.Model):
    title = models.CharField(max_length=200, default="Your title")
    text = models.TextField(default="Your review")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    visible = models.BooleanField(default=False)#admin must approve each review first

    Rating_CHOICES = (
        (1, 'Poor'),
        (2, 'Average'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent')
    )
    rating = models.IntegerField(choices=Rating_CHOICES, default=0)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'book',)
    list_filter = ('user', 'book',)
    fields = ('title', 'book', 'text', 'visible', 'user', )
    list_display_links = ('title', 'book',)
    readonly_fields = ('user',)
