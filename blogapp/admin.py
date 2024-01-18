from django.contrib import admin
from .models import Category, Blog, Comment, PostView, Like

admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(PostView)
admin.site.register(Like)