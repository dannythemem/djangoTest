from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
import uuid, os

from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from men.forms import AddPostForm, UploadFileForm
from men.models import Men, Category, UploadFiles
from men.utils import DataMixin

# menu = [
#     {'title': "О сайте", 'url_name': 'about'},
#     {'title': "Добавить статью", 'url_name': 'add_page'},
#     {'title': "Обратная связь", 'url_name': 'contact'},
#     {'title': "Войти", 'url_name': 'login'}
# ]

# Create your views here.
# def index(request): #ссылка на класс HttpRequest
#     # t = render_to_string('men/index.html')
#     # return HttpResponse(t)
#     posts = Men.published.all().select_related('cat') #жадная загрузка(для избегания дублирования sql запросов)
#
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'men/index.html', context=data)

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

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             #print(form.cleaned_data)
#             # try:
#             #     Men.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()
#             return redirect('home')
#     else:
#
#         form = AddPostForm()
#
#     data = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form': form
#     }
#     return render(request, 'men/addpage.html', data)

# def show_post(request, post_slug):
#     post = get_object_or_404(Men, slug=post_slug)
#     #Функция get_object_or_404() в Django — это удобный шорткат, который помогает извлечь объект из базы данных и автоматически выбрасываетошибку404, если объект ненайден.
#     #Это избавляет от необходимости писать try/ except вручную.
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#     return render(request, 'men/post.html', data)

# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#         return render(request, 'men/addpage.html', data)
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#         return render(request, 'men/addpage.html', data)

# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Men.published.filter(cat_id = category.pk).select_related('cat')
#
#     data = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#     return render(request, 'men/index.html', context=data)

def about(request):
    # if request.method == 'POST':
    #     # handle_uploaded_file(request.FILES['file_upload'])
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         # handle_uploaded_file(form.cleaned_data['file'])
    #         fp = UploadFiles(file = form.cleaned_data['file'])
    #         fp.save()
    # else:
    #     form = UploadFileForm()

    contact_list = Men.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'men/about.html', {'title': 'О сайте', 'page_obj': page_obj})


class MenHome(DataMixin, ListView):
    template_name = 'men/index.html'
    context_object_name = 'posts' #по умолчанию object_list
    #По умолчанию <имя приложения> / < имя модели > _list.html т.е. men/men_list.html
    title_page = 'Главная страница'
    cat_selected = 0


    def get_queryset(self):
        return Men.published.all().select_related('cat')


class ShowPost(DataMixin, DetailView):
    model = Men
    template_name = 'men/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title = context["post"].title)


    def get_object(self, queryset=None):
        return get_object_or_404(Men.published, slug=self.kwargs[self.slug_url_kwarg])


class MenCategory(DataMixin, ListView):
    template_name = 'men/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Men.published.filter(cat__slug = self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context["posts"][0].cat
        return  self.get_mixin_context(context, title = 'Категория - ' + cat.name, cat_selected = cat.pk)


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'men/addpage.html'
    title_page = 'Добавление статьи'


class UpdatePage(DataMixin, UpdateView):
    model = Men
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'men/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'


class DeletePage(DataMixin, DeleteView):
    model = Men
    success_url = reverse_lazy('home')
    template_name = 'men/men_confirm_delete.html'
    context_object_name = 'post'
    title_page = 'Удаление статьи'


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


