from django.contrib import admin
from .models import Article, Category

class ArticleInLine(admin.TabularInline):
    model = Article

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        ArticleInLine
    ]
    list_display = ('name', )

admin.site.register(Category, CategoryAdmin)
