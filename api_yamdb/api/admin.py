from django.contrib import admin

from reviews.models import Genre


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


admin.site.register(Genre, GenreAdmin)
