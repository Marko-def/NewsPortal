from django.contrib.auth.mixins import UserPassesTestMixin

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()