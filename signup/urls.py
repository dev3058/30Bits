from django.urls import path
from .import views
from django.contrib.auth import forms, views as auth_views
from .forms import SetPasswordForm
urlpatterns = [
    path('signup/',views.signup, name='signup-page'),
    path('activate-user/<slug:uid64>/<slug:token>/',views.activate_user,name='activate'),
    path('user-login/',views.userlogin,name='user-login-page'),
    path('user-profile-update/',views.userprofile,name='user-profile-update'),
    path('reset_password/',views.PasswordReset, name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name = "signup/password-recovery/password_reset_sent.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = "signup/password-recovery/password_reset_confirm.html", form_class = SetPasswordForm),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name = "signup/password-recovery/password_reset_complete.html"),name='password_reset_complete'),

    path('password-change',views.ChangePassword,name = 'change-password'),

    path('logout/',auth_views.LogoutView.as_view(next_page = '/user/user-login'),name='logout-action'),
    
]
 