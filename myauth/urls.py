from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .views import (
    MyAccountDetailView,
    MyAccountUpdateView,
    UserRegistrationView,
    EmailConfirmationSentView,
    UserConfirmEmailView,
    EmailConfirmedView,
    EmailConfirmationFailedView,
    MyLoginView,
)

app_name = 'myauth'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('email_confirmation_sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm_email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email_confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('email_confiramation_failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),

    path(
        'login/',
        MyLoginView.as_view(
            template_name='myauth/login.html',
            redirect_authenticated_user=True,
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
            success_url=reverse_lazy('myauth:password_reset_done'),
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

    path('my_account/<int:pk>/', MyAccountDetailView.as_view() , name='my_account'),
    path('my_account/update/', MyAccountUpdateView.as_view(), name='my_account_update'),
]
