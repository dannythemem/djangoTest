from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from men.models import Men, Category

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
]

# Create your views here.
def index(request): #ссылка на класс HttpRequest
    # t = render_to_string('men/index.html')
    # return HttpResponse(t)
    posts = Men.published.all().select_related('cat') #жадная загрузка(для избегания дублирования sql запросов)

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'men/index.html', context=data)


def about(request):
    return render(request, 'men/about.html', {'title': 'О сайте', 'menu': menu})


def show_post(request, post_slug):
    post = get_object_or_404(Men, slug=post_slug)
    #Функция get_object_or_404() в Django — это удобный шорткат, который помогает извлечь объект из базы данных и автоматически выбрасываетошибку404, если объект ненайден.
    #Это избавляет от необходимости писать try/ except вручную.
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'men/post.html', data)


def addpage(request):
    return HttpResponse('Добавление статьи')


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


def show_category(request, cat_slug):
    categoty = get_object_or_404(Category, slug=cat_slug)
    posts = Men.published.filter(cat_id = categoty.pk).select_related('cat')

    data = {
        'title': f'Рубрика: {categoty.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': categoty.pk,
    }
    return render(request, 'men/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


