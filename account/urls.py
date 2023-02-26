from django.urls import re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'account'
urlpatterns = [
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='registration/sign_in.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(template_name='registration/sign_out.html'), name='logout'),
    re_path(r'^register/$', views.register, name='register'),
    #Password change.
    re_path(r'^password-change/$', login_required(auth_views.PasswordChangeView.as_view(template_name='registration/passwordChangeForm.html')), name='passwordChange'),
    re_path(r'^password-change/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='registration/passwordChangeDone.html'), name='passwordChangeDone'),
    #Password reset.
    re_path(r'^password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/passwordResetForm.html'), name='passwordReset'),
    re_path(r'^password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/passwordResetDone.html'), name='passwordResetDone'),
    re_path(r'^reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/passwordResetConfirm.html'), name='passwordResetConfirm'),
    re_path(r'^reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/passwordResetComplete.html'), name='passwordResetComplete'),
    #delete account
    re_path(r'^delete-account/$', views.deleteAccount, name='deleteAccount'),
    re_path(r'^profile/$', views.profile, name='profile'),
    re_path(r'^edit-profile/$', views.editProfile, name='editProfile'),
    
]
