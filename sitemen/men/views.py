from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
import uuid
import os
from men.forms import AddPostForm, UploadFileForm
from men.models import Men, Category, UploadFiles

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

# def handle_uploaded_file(f):
#     upload_dir = 'uploads'
#     base_name, ext = os.path.splitext(f.name)
#     new_name = f.name
#     file_path = os.path.join(upload_dir, f.name)
#
#     if os.path.exists(file_path):
#         new_name = f'{base_name}_{uuid.uuid4()}{ext}'
#
#     new_file_path = os.path.join(upload_dir, new_name)
#
#     with open(new_file_path, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)



def about(request):
    if request.method == 'POST':
        # handle_uploaded_file(request.FILES['file_upload'])
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file = form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'men/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})


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
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)

        if form.is_valid():
            #print(form.cleaned_data)
            # try:
            #     Men.objects.create(**form.cleaned_data)
            #     return redirect('home')
            # except:
            #     form.add_error(None, 'Ошибка добавления поста')
            form.save()
            return redirect('home')
    else:

        form = AddPostForm()

    data = {
        'menu': menu,
        'title': 'Добавление статьи',
        'form': form
    }
    return render(request, 'men/addpage.html', data)


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


