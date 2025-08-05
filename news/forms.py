from django import forms
from .models import Author

class NewsForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['title', 'content', 'author']  # Не включаем поле type