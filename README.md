# Импортируем необходимые модели
from django.contrib.auth.models import User
from myapp.models import Author, Category, Post, Comment

# Создаем двух пользователей
user1 = User.objects.create_user('user1', password='password1')
user2 = User.objects.create_user('user2', password='password2')

# Создаем авторов, связанных с пользователями
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# Добавляем категории
category1 = Category.objects.create(name='Спорт')
category2 = Category.objects.create(name='Политика')
category3 = Category.objects.create(name='Образование')
category4 = Category.objects.create(name='Технологии')

# Добавляем статьи и новости
post1 = Post.objects.create(author=author1, post_type=Post.ARTICLE, title='Статья о спорте', text='Текст статьи о спорте.')
post2 = Post.objects.create(author=author2, post_type=Post.NEWS, title='Новости политики', text='Текст новостей политики.')

# Присваиваем категории
post1.categories.add(category1, category3)  # Статья о спорте имеет категории Спорт и Образование
post2.categories.add(category2)  # Новости политики имеют категорию Политика

# Создаем комментарии к постам
comment1 = Comment.objects.create(post=post1, user=user1, text='Отличная статья!')
comment2 = Comment.objects.create(post=post1, user=user2, text='Очень интересно!')
comment3 = Comment.objects.create(post=post2, user=user1, text='Интересные новости!')
comment4 = Comment.objects.create(post=post2, user=user2, text='Неплохая статья.')

# Применяем функции like() и dislike() к постам и комментариям
post1.like()
post1.like()
post2.dislike()
comment1.like()
comment2.dislike()

# Обновляем рейтинги авторов
author1.update_rating()
author2.update_rating()

# Выводим username и рейтинг лучшего пользователя
best_author = Author.objects.order_by('-rating').first()
print(best_author.user.username, best_author.rating)

# Выводим данные о лучшей статье
best_post = Post.objects.order_by('-rating').first()
print(best_post.created_at, best_post.author.user.username, best_post.rating, best_post.title, best_post.preview())

# Выводим все комментарии к лучшей статье
for comment in best_post.comment_set.all():
    print(comment.created_at, comment.user.username, comment.rating, comment.text)
