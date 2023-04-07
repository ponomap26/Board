# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
from django.core.cache import cache
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView


from .filters import BlogFilter
from .forms import BordForm
from .models import Ad, Author, Profile


class BlogsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Ad
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'created_at'
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

    # def get_object(self, *args, **kwargs):
    #     obj = cache.get(f'blog{self.kwargs["pk"]}', None)
    #
    #     if not obj:
    #         obj = super().get_object(queryset=self.queryset)
    #         cache.set(f'blog{self.kwargs["pk"]}', obj)
    #         # print("2222")
    #     else:
    #         print("Кешь есть")
    #     return obj


class BlogsSearch(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Ad
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'created_at'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'search'
    paginate_by = 2

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        self.filterset = BlogFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['all_blogs'] = Ad.objects.all()
        return context

class BlogsCreate(LoginRequiredMixin, CreateView):
    form_class = BordForm
    raise_exception = True
    permission_required = ('blogs.add_blog',)
    model = Ad
    template_name = 'create.html'
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        # Получаем текущего пользователя
        user = self.request.user
        # Проверяем, есть ли объект Author для этого пользователя
        try:
            author = Author.objects.get(authorUser=user)
        except Author.DoesNotExist:
            # Если объект Author не существует, создаем его
            author = Author.objects.create(authorUser=user)
        # Устанавливаем созданного автора для формы Ad
        form.instance.author = author
        return super().form_valid(form)





class CategoryListView(BlogsList):
    model = Ad
    template_name = 'category_list.html'
    context_object_name = 'category_blogs_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Ad.objects.filter(category=self.category).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        print(f'{context = }')
        context['categories'] = self.category

        return context