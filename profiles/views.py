from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, UpdateView

from .models import *
from .forms import ProfileForm


class ProfileDetail(LoginRequiredMixin, DetailView):
    '''Вывод профиля пользователя'''
    model = Profile
    context_object_name = 'profile'
    template_name = 'profiles/profile_detail.html'


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    '''Редактирование профиля'''
    form_class = ProfileForm
    model = Profile
    template_name = 'profiles/profile_update.html'

    def form_valid(self, form):
        return super().form_valid(form)




