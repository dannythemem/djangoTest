from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, CreateView, UpdateView
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from django.core.exceptions import PermissionDenied

# Create your views here.


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {
        'title': 'Профиль пользователя',
        'default_image': settings.DEFAULT_USER_IMAGE,
    }

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

class UserPasswordChange(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('users.social_auth'):
            raise PermissionDenied('Отказано в доступе. Вы вошли через социальные сети, поэтому, вы не можете изменить пароль ')
        return super().dispatch(request, *args, **kwargs)