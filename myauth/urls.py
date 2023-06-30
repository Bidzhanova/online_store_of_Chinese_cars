from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .views import my_account
from .forns import UserLoginForm

app_name = 'myauth'

urlpatterns = [

    path(
        'login/',
        LoginView.as_view(
            template_name='myauth/login.html',
            redirect_authenticated_user=True,
            authentication_form=UserLoginForm,
        ),
        name='login'
    ),

    path('logout/', LogoutView.as_view(), name='logout'),

    path(
        'password_change/',
        PasswordChangeView.as_view(
            template_name='myauth/password_change.html',
            success_url=reverse_lazy('myauth:password_change_done')
        ),
        name='password_change'
    ),

    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='myauth/password_change_done.html',
        ),
        name='password_change_done'
    ),

    path(
        'password_reset/',
        PasswordResetView.as_view(
            template_name='myauth/password_reset.html',
            email_template_name='myauth/password_reset_email.html',
            success_url=reverse_lazy('myauth:password_reset_done')
        ),
        name='password_reset'
    ),

    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='myauth/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='myauth/password_reset_confirm.html',
            success_url=reverse_lazy('myauth:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='myauth/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    path('my_account/', my_account, name='my_account'),
]
