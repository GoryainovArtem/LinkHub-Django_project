from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = 'urls'


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout')
]
