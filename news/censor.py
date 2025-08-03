from django import template

register = template.Library()

# Список нецензурных слов
BAD_WORDS = ['редиска']


@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр censor может применяться только к строкам.")

    for word in BAD_WORDS:
        censored_word = word[0] + '*' * (len(word) - 1)
        value = value.replace(word, censored_word)
        value = value.replace(word.capitalize(), censored_word.capitalize())

    return value