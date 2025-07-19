from django.contrib import admin
from .models import Men, Category


@admin.register(Men)
class MenAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'time_created', 'is_published', 'cat']
    list_display_links = ('id', 'title')
    ordering = ('time_created', 'title')
    list_editable = ('is_published', )
    list_per_page = 5

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']

# admin.site.register(Men, MenAdmin)
