from django import template
from django.db.models import Count

import men.views as views
from men.models import Category, TagPost
register = template.Library()

@register.simple_tag(name = 'get_cats')
def get_categories():
    return views.cats_db

@register.inclusion_tag('men/list_categories.html')
def show_categories(cat_selected = 0):
    cats =  Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('men/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.annotate(total=Count('tag')).filter(total__gt=0)}
