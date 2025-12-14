from django.contrib import admin

from .models import Author, Category, Post, Comment, About, Tag

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(About)
