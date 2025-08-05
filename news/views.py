from django.shortcuts import reverse_lazy,render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.core.paginator import Paginator
from .filters import AuthorFilter
from .models import Author
from .forms import NewsForm


def news_list(request):
    news = Author.objects.all()  # Получаем все новости
    return render(request, 'news/news_list.html', {'news': news})

def news_detail(request, id):
    news_item = get_object_or_404(Author, id=id)  # Получаем конкретную новость по ID
    return render(request, 'news/news_detail.html', {'news_item': news_item})


def news_list(request):
    news_filter = AuthorFilter(request.GET, queryset=Author.objects.all())
    paginator = Paginator(news_filter.qs, 10)  # Показывать 10 новостей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_list.html', {'filter': news_filter, 'page_obj': page_obj})


class NewsCreate(CreateView):
    form_class = NewsForm
    template_name = 'news/news_form.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'news'  # Устанавливаем тип как 'news'
        news.save()
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = NewsForm
    template_name = 'articles/article_form.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.type = 'article'  # Устанавливаем тип как 'article'
        article.save()
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    model = Author
    form_class = NewsForm
    template_name = 'news/news_form.html'


class ArticleUpdate(UpdateView):
    model = Author
    form_class = NewsForm
    template_name = 'articles/article_form.html'


class NewsDelete(DeleteView):
    model = Author
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleDelete(DeleteView):
    model = Author
    template_name = 'articles/article_delete.html'
    success_url = reverse_lazy('news_list')  # Перенаправляем на список новостей/статей