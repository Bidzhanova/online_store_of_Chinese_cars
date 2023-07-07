from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

class UserRegistrationForm(UserCreationForm):
    """Форма регистрации пользователей на сайте."""
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        """Проверка email на уникальность."""
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован на сайте.')
        return email

class UserUpdateForm(forms.ModelForm):
    """Форма обновления данных о пользователе."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)

    def clean_email(self):
        """Проверка email на уникальность."""
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username', '')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email должен быть уникальным.')
        return email

class ProfileUpdateForm(forms.ModelForm):
    """Форма обновления данных профиля пользователя."""
    class Meta:
        model = Profile
        fields = ('avatar', 'birth_date', 'bio',)
