from django_filters import FilterSet, DateTimeFilter, CharFilter
from django.forms import DateTimeInput
from .models import Ad, Response


class BlogFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='created_at',
        lookup_expr='gt',
        label="Дата публикации не позднее",
        widget=DateTimeInput(
            format='%Y-%m-%d',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Ad
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            'title': ['icontains'],
            'category': ['exact'],
        }


class ResponseFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='created_at',
        lookup_expr='gt',
        label="Дата публикации не позднее",
        widget=DateTimeInput(
            format='%Y-%m-%d',
            attrs={'type': 'datetime-local'},
        )
    )
    title = CharFilter(
        field_name='title',
        lookup_expr='exact',
        label='Заголовок объявления'
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Ad
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = ["title"]