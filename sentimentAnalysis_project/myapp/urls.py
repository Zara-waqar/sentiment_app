from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from .views import create_sentence, update_sentence, delete_sentence
urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_success'), name='logout'),
    path('home/',views.index, name='index'),
    path('logout_success/', views.logout, name='logout_success'),
    path('signup/', views.signup_view, name='signup'),
    path('create_sentence/', create_sentence, name='create_sentence'),
    # path('view_sentences/', view_sentences, name='view_sentences'),
    path('update_sentence/<int:id>/', update_sentence, name='update_sentence'),
    path('delete_sentence/<int:id>/', delete_sentence, name='delete_sentence'),
    ]
