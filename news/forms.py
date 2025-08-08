from django import forms
from .models import News
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'author']

class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user
