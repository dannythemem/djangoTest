from django import template
import men.views as views
from men.models import Category
register = template.Library()

@register.simple_tag(name = 'get_cats')
def get_categories():
    return views.cats_db

@register.inclusion_tag('men/list_categories.html')
def show_categories(cat_selected = 0):
    cats =  Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}
