from django.contrib import admin
from main.models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.


@admin.register(Novel)
class NovelAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display = ['id', 'name', 'date', 'lang']


@admin.register(Chapters)
class ChaptersAdmin(ImportExportModelAdmin):
    search_fields = ['title', 'chapter', 'date']
    list_display = ['title', 'id', 'date', 'chapter']


@admin.register(ColNovel)
class ColNovelAdmin(ImportExportModelAdmin):
    search_fields = ['title']
    list_display = ['id', 'title']


@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'id']
