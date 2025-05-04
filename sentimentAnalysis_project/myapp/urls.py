from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from .views import create_sentence, update_sentence, delete_sentence
urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/',views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('create_sentence/', create_sentence, name='create_sentence'),
    path('update_sentence/<int:id>/', update_sentence, name='update_sentence'),
    path('delete_sentence/<int:id>/', delete_sentence, name='delete_sentence'),
    ]
