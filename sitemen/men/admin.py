from django.contrib import admin, messages
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
    list_display = ['title', 'time_created', 'is_published', 'cat', 'brief_info']
    list_display_links = ('title', )
    ordering = ('time_created', 'title')
    list_editable = ('is_published', )
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = [MarriedFilter, 'cat__name', 'is_published']

    @admin.display(description = 'Краткое описание', ordering='content')
    def brief_info(self, men: Men):
        return f'Описание {len(men.content)} символов'

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
