from django.contrib import admin

from reviews.models import Category, Genre, Title, TitleGenre, Comment, Review


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    list_editable = ('name', 'slug',)
    search_fields = ('name', 'slug',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    list_editable = ('name', 'slug',)
    search_fields = ('name', 'slug',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category',)
    list_editable = ('name', 'year', 'description',)
    search_fields = ('name', 'year',)
    list_filter = ('name', 'year', 'genre', 'category')
    empty_value_display = '-пусто-'


class TitleGenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'genre',)
    list_editable = ('title', 'genre',)
    search_fields = ('title', 'genre',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text',)
    list_editable = ('title', 'text',)
    search_fields = ('title', 'text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text',)
    list_editable = ('review', 'text',)
    search_fields = ('review', 'text',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(TitleGenre, TitleGenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
