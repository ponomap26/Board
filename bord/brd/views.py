from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .filters import BlogFilter
from .forms import BordForm, ResponseForm
from .models import Ad, Author, Profile, Response


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
        # Создаем объект Ad, но не сохраняем его пока
        ad = form.save(commit=False)
        # Проверяем, есть ли объект Author для этого пользователя
        try:
            author = Author.objects.get(authorUser=user)
        except Author.DoesNotExist:
            # Если объект Author не существует, создаем его
            author = Author.objects.create(authorUser=user)
        # Устанавливаем созданного автора и пользователя для Ad
        ad.author = author
        ad.created_by = user.profile
        # Сохраняем объект Ad
        ad.save()
        return super().form_valid(form)


@login_required
def add_response(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.created_by = request.user.profile  # использование модели Profile
            response.ad = ad
            response.save()
            return redirect('add_response', ad_id=ad_id)
    else:
        form = ResponseForm()
    context = {'form': form, 'ad': ad}
    return render(request, 'add_response.html', context)


def add_comment_view(request, ad_id):
    """
    Обработчик формы добавления комментария.
    """
    ad = Ad.objects.get(id=ad_id)

    if request.method == 'POST':
        form = ResponseForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            body = form.cleaned_data['body']

            comment = Response.objects.create(
                ad=ad,
                name=name

            )

            return redirect('blog', blog_id=ad.blog.id)

    else:
        form = ResponseForm()

    return render(request, 'add_comment.html', {'form': form})
