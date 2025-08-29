from django.urls import path, re_path, register_converter
from . import views # . - тк импортрируем из текущей папки
from . import converters
from django.views.decorators.cache import cache_page

register_converter(converters.ForDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.MenHome.as_view(), name = 'home'), #http://127.0.0.1:8000
    path('about/', views.about, name = 'about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.MenCategory.as_view(), name='category'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
    path('delete/<int:pk>/', views.DeletePage.as_view(), name='delete_page'),

]


