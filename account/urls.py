from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.urls import path, reverse_lazy

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/registration/login.html'), name='login'),
    path('logout/',views.log_out,name='logout'),
    path('register/',views.register,name='register'),
    path('password-reset/',PasswordResetView.as_view(template_name='account/registration/password_reset.html',email_template_name='account/registration/password_reset_email.html',success_url=reverse_lazy('account:password_reset_done')),name='reset_password'),
    path('password-reset/done/',PasswordResetDoneView.as_view(template_name='account/registration/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name='account/registration/password_reset_confirm.html',success_url=reverse_lazy('account:password_reset_complete')),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='account/registration/password_reset_complete.html'),name='password_reset_complete'),
    path('change password/',views.change_password,name='change_password'),
    path('wallet/',views.wallet,name='wallet'),
    path('Wallet-recharge/',views.wallet_recharge,name='wallet_recharge'),
    path('wallet-transaction/',views.wallet_transaction,name='wallet_transaction'),
]

