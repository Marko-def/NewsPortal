from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import PostCategory, News
from django.template.loader import render_to_string
from django.urls import reverse
from celery import shared_task
from django.core.mail import send_mail
from .models import Subscriber, News


def notify_subscribers(news):
    # Получаем всех подписчиков на категорию новости
    subscribers = news.category.subscribers.all()
    subject = f'Новая новость в категории {news.category.name}'

    for subscriber in subscribers:
        message = f"""Здравствуйте, {subscriber.user.username}!\n\n
        В категории "{news.category.name}" появилась новая новость:\n
        Title: {news.title}\n
        Content: {news.content[:100]}...\n\n
        Перейдите по ссылке, чтобы прочитать полностью: http://yourwebsite.com/news/{news.id}
        """

        send_mail(
            subject,
            message,
            from_email='your_email@example.com',
            recipient_list=[subscriber.user.email],
        )


def send_welcome_email(user):
    subject = 'Добро пожаловать в наш сайт!'
    activation_link = reverse('activate_account', args=[user.activation_token])

    message = render_to_string('emails/welcome_email.html', {
        'username': user.username,
        'activation_link': activation_link,
    })

    send_mail(
        subject,
        message,
        from_email='your_email@example.com',
        recipient_list=[user.email],
        html_message=message,
    )


def notify_subscriber(news):
    # Получаем всех подписчиков на категорию новости
    subscribers = news.category.subscribers.all()

    for subscriber in subscribers:
        subject = f'Новая статья: {news.title}'

        message = render_to_string('emails/news_notification.html', {
            'news_title': news.title,
            'news_content': news.content[:50] + '...',
            'username': subscriber.user.username,
            'news_link': f"http://yourwebsite.com/news/{news.id}",
        })

        send_mail(
            subject,
            message,
            from_email='your_email@example.com',
            recipient_list=[subscriber.user.email],
            html_message=message,
        )

@shared_task
def send_notification(news_id):
    news = News.objects.get(id=news_id)
    subscribers = Subscriber.objects.all()
    for subscriber in subscribers:
        send_mail(
            subject=f'Новое сообщение: {news.title}',
            message=news.content,
            from_email='your_email@example.com',
            recipient_list=[subscriber.email],
        )

@shared_task
def weekly_newsletter():
    news = News.objects.filter(created_at__week=timezone.now().isocalendar()[1])  # Получение новостей за текущую неделю
    subscribers = Subscriber.objects.all()
    for subscriber in subscribers:
        send_mail(
            subject='Последние новости за неделю',
            message='\n'.join([news_item.title for news_item in news]),
            from_email='your_email@example.com',
            recipient_list=[subscriber.email],
        )
