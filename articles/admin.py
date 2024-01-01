from tokenize import Comment
from django.contrib import admin
from .models import Articles, Comments

class CommentInline(admin.TabularInline):
    model = Comments

class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]

admin.site.register(Articles, ArticleAdmin)
admin.site.register(Comments)

