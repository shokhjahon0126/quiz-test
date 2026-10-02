from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_home_view, name='quiz_home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/open/<int:question_number>/', views.open_question_view, name='open_question'),
    path('reset/', views.reset_quiz_view, name='reset_quiz'),
]
