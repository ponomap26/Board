from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView

from bord.brd.models import Ad


class BlogsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Ad
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dataCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'blogs.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'blogs'
    paginate_by = 10


class BlogsDetail(DetailView):
    model = Ad
    template_name = 'blog.html'
    context_object_name = 'blog'
    queryset = Ad.objects.all()

class BlogsSearch(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Ad
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'dataCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'search'
    paginate_by = 10




# class BlogsCreate(PermissionRequiredMixin, CreateView):
#     form_class = NewsForm
#     raise_exception = True
#     permission_required = ('blogs.add_blog',)
#     model = Ad
#     template_name = 'blods_create.html'