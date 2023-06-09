from django.contrib import messages
from django.contrib.auth.models import User
from django.core.signals import request_finished
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import ValidationError, PermissionDenied

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .filters import BlogFilter, ResponseFilter
from .forms import BordForm, ResponseForm, BlogsDelete, BlogsEdit
from .models import Ad, Author, Response


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


class BlogsCreate(PermissionRequiredMixin, CreateView):
    form_class = BordForm
    raise_exception = True
    permission_required = ('blogs.add_blog',)
    model = Ad
    template_name = 'create.html'
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        # Получаем текущего пользователя
        user = self.request.user
        # Создаем объект Ad, но не сохраняем его пока
        ad = form.save(commit=False)
        # Проверяем, есть ли объект Author для этого пользователя
        try:
            author = Author.objects.get(authorUser=user)
        except Author.DoesNotExist:
            # Если объект Author не существует, создаем его
            author = Author.objects.create(authorUser=user)
        # Устанавливаем созданного автора и пользователя для Ad
        ad.author = user
        ad.created_by = user.profile
        # Сохраняем объект Ad
        ad.save()
        return super().form_valid(form)


class BlogsDelete(LoginRequiredMixin, DeleteView):
    # permission_required = ('blogs.delete_blog',)
    form_class = BlogsDelete
    model = Ad
    template_name = 'blogs_delete.html'
    success_url = reverse_lazy('blogs')


class BlogsUpdate(LoginRequiredMixin, UpdateView):
    raise_exception = True
    # permission_required = ('blogs.change_blog',)
    form_class = BlogsEdit
    model = Ad
    template_name = 'blogs_edit.html'
    success_url = reverse_lazy('blogs')

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("description")
        if title is not None and len(title) > 15:
            raise ValidationError({
                "Название ": "Название не может быть больше 15 символов."
            })

        return cleaned_data


def form_valid(self, form):
    # получить пользователя. Если Нет -> 404
    author = form.save(commit=False)
    if self.request.user.username:
        author.author = User.objects.get(username=self.request.user.username)
    else:
        return HttpResponseRedirect('../404/')

    return super().form_valid(form)


"""ОТЗЫВЫ"""


class ResponseList(LoginRequiredMixin, ListView):
    model = Response
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'created_at'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'ad_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'response_list'
    paginate_by = 10


class ResponseDetail(DetailView):
    model = Response
    template_name = 'response_detail.html'
    context_object_name = 'response_detail'
    queryset = Response.objects.all()


class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'response_delete.html'
    success_url = reverse_lazy('user_responses')
    raise_exception = True

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.author == self.request.user:
            if not self.request.user.is_superuser:
                raise PermissionDenied
        return obj


class ResponseSearch(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Ad
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'created_at'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'response_search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'response_search'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        self.filterset = ResponseFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filtersets'] = self.filterset
        # context['all_blogs'] = Ad.objects.all()
        return context


class UserResponseListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'user_response_list.html'
    context_object_name = 'responses'
    paginate_by = 10

    def get_queryset(self):
        return Response.objects.filter(ad__created_by__user=self.request.user)


@login_required
def add_response(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.author = request.user
            response.ad = ad
            response.save()
            return redirect('blog', pk=pk)
    else:
        form = ResponseForm()

    return render(request, 'add_response.html', {'ad': ad, 'form': form})


# @require_POST
# def delete_response(request, response_id):
#     response = get_object_or_404(Response, id=response_id, author=request.user)
#     response.delete()
#     return redirect('user_responses')


def accept_response(request, response_id):
    response = get_object_or_404(Response, pk=response_id)
    if response.accepted:
        # Отзыв уже принят, выводим сообщение об ошибке
        messages.error(request, 'Отзыв уже был принят')
    else:
        response.accepted = True
        response.save()
        messages.success(request, 'Отзыв успешно принят')

    return redirect('user_responses')
