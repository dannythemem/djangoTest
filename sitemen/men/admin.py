from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Men, Category


class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус мужчин'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Женат'),
            ('single', 'Холост')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(wife__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(wife__isnull=True)
        


@admin.register(Men)
class MenAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'photo', 'post_photo', 'slug', 'cat', 'wife', 'tags']
    #exclude = ['tags', 'is_published']
    readonly_fields = ['post_photo']
    list_display = ['title', 'post_photo', 'time_created', 'is_published', 'cat']
    filter_horizontal = ['tags']
    list_display_links = ('title', )
    ordering = ('time_created', 'title')
    list_editable = ('is_published', )
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = [MarriedFilter, 'cat__name', 'is_published']
    save_on_top = True

    @admin.display(description = 'Изображения', ordering='content')
    def post_photo(self, men: Men):
        if men.photo:
            return mark_safe(f'<img src="{men.photo.url}" width="50" />')
        return 'Без фото'

    @admin.action(description = 'Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Men.Status.PUBLISHED)
        self.message_user(request, f'{count} записей снято с публикации')

    @admin.action(description = 'Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Men.Status.DRAFT)
        self.message_user(request, f'Изменено {count} записей', messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']

# admin.site.register(Men, MenAdmin)
