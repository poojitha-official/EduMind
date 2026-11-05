from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('topic-explainer/', views.topic_explainer, name='topic_explainer'),
    path('chat/', views.chat, name='chat'),
    path('interview-prep/', views.interview_prep, name='interview_prep'),
    path('quiz_generator/', views.quiz_generator, name='quiz_generator'),
    path('history/', views.history, name='history'),
]