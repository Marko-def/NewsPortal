from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .filters import AuthorFilter
from .models import Author,Post,Category,News
from .forms import NewsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .mixins import AuthorRequiredMixin
from .tasks import notify_subscribers

def create_news(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category_id = request.POST['category']

        news = News(title=title, content=content, category_id=category_id, author=request.user)

        if news.is_user_limit_exceeded():
            return render(request, 'create_news.html', {'error': 'Вы не можете публиковать более 3 новостей в сутки.'})

        news.save()
        notify_subscribers(news)  # Уведомляем подписчиков

        return redirect('news_list')  # Перенаправляем на список новостей

    return render(request, 'create_news.html')

def subscribe_to_category(request, category_id):
    if request.user.is_authenticated:
        category = get_object_or_404(Category, id=category_id)
        category.subscribers.add(request.user)
        return redirect('category_detail', category_id=category.id)
    else:
        return redirect('login')

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


class ArticleUpdate(LoginRequiredMixin,UpdateView):
    model = Author
    form_class = NewsForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('article_list')


class NewsDelete(DeleteView):
    model = Author
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleDelete(DeleteView):
    model = Author
    template_name = 'articles/article_delete.html'
    success_url = reverse_lazy('news_list')  # Перенаправляем на список новостей/статей

@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    user.groups.add(authors_group)
    return redirect('home')


class PostCreateView(AuthorRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(AuthorRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post_form.html'
