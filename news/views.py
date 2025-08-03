from django.shortcuts import render, get_object_or_404
from .models import Author

def news_list(request):
    news = Author.objects.all()  # Получаем все новости
    return render(request, 'news/news_list.html', {'news': news})

def news_detail(request, id):
    news_item = get_object_or_404(Author, id=id)  # Получаем конкретную новость по ID
    return render(request, 'news/news_detail.html', {'news_item': news_item})