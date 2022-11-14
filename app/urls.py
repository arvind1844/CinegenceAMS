from . import views
from django.urls import path
from app.views import ResetPasswordView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path('all_assets/',views.all_assets,name='all_assets'),
    path('form_details/<str:id>',views.form_details,name='form_details'),
    path('individual_asset/<int:id>',views.individual_asset,name='individual_asset'),
    path('contact/',views.contact,name='contact'),
    path('register/', views.register, name='register' ),
    path('timer/<str:id>',views.timer,name='timer'),
    path('logout/',views.logout_view,name='logout'),
    path('user_profile/',views.UpdateProfileView,name='user_profile'),
    path('terms/',views.terms, name='terms'),
    # path('profile/', views.ProfileView, name='profile'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),

]
