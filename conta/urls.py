from django.urls import path
from . import views


app_name = 'conta'

urlpatterns = [
    path('register/', views.register_view, name='register-view'),
    path('login/', views.login_view, name='login-view'),
    path('logout/', views.logout_view, name='logout-view'),
]
