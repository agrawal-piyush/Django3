from django.urls import path
from . import views

from django.contrib.auth import views as  auth_views
urlpatterns=[

path('',views.dashboard,name='dashboard'),
path('Login/',auth_views.LoginView.as_view(), name='login'),
path('Logout/',auth_views.LogoutView.as_view(),name='logout'),
path ('register/',views.register,name='register'),

#reset password
path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
#sentiment
path('SA/',views.SAF,name='saf'),
path('Record/',views.Record,name='record')


]
