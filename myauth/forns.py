from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    """
    Форма авторизации на сайте
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин или эл. почта'
        self.fields['password'].label = 'Пароль'
