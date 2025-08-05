import django_filters
from .models import Author

class AuthorFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Название')
    author = django_filters.CharFilter(lookup_expr='icontains', label='Автор')
    published_date = django_filters.DateFilter(widget=django_filters.widgets.DateInput(attrs={'type': 'date'}), label='Дата публикации', lookup_expr='gte')

    class Meta:
        model = Author
        fields = ['title', 'author', 'published_date']