import django_filters
from django.forms.widgets import DateInput
from .models import Author

class AuthorFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Название')
    author = django_filters.CharFilter(lookup_expr='icontains', label='Автор')
    published_date = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}), label='Дата публикации', lookup_expr='gte')

    class Meta:
        model = Author
        fields = ['title', 'author', 'published_date']