"""
URL configuration for sitemen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

from men.sitemaps import PostSitemap
from men.views import page_not_found
from sitemen import settings
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('men.urls')), #http://127.0.0.1:8000
    path('users/', include('users.urls', namespace='users')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('captcha/', include('captcha.urls')),
    path('sitemap.xml', cache_page(60*60*24)(sitemap), {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) #только для режима отладки
    

handler404 = page_not_found

admin.site.site_header = 'Панель Администрирования'
admin.site.index_title = 'Известные мужчины мира'
