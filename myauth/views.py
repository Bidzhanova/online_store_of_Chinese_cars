from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView

from .forns import UserRegistrationForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile


class MyAccountDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'myauth/my_account.html'
    context_object_name = 'profile'

class MyAccountUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'myauth/my_account_update.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(MyAccountUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('myauth:my_account', kwargs={'pk': self.object.pk})


class MyLoginView(LoginView):
    """Представление аутентификации пользователя на сайте."""
    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse('myauth:my_account', kwargs={'pk': self.request.user.pk})


class UserRegistrationView(CreateView):
    """Представление регистрации пользователя на сайте."""
    form_class = UserRegistrationForm
    template_name = 'myauth/user_registration.html'
    success_url = reverse_lazy('myauth:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        profile = Profile.objects.create(user=user)
        profile.user.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('myauth:confirm_email', kwargs={'uidb64': uid, 'token': token})
        current_site = Site.objects.get_current()
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}',
            'cars.auth@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return redirect(reverse('myauth:email_confirmation_sent'))


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect(reverse('myauth:email_confirmed'))
        else:
            return redirect(reverse('myauth:email_confirmation_failed'))


class EmailConfirmationSentView(TemplateView):
    """Представление уведомления об отправке письма для подтверждения по электронной почте."""
    template_name = 'myauth/email_confirmation_sent.html'


class EmailConfirmedView(TemplateView):
    """Представление успешного подтверждения электронной почты."""
    template_name = 'myauth/email_confirmed.html'


class EmailConfirmationFailedView(TemplateView):
    """Представление ошибки подтверждения по электронной почте."""
    template_name = 'myauth/email_confirmation_failed.html'
