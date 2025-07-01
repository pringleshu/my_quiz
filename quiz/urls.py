from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    # 메인 페이지
    path('', views.home, name='home'),
    
    # 퀴즈 관련
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('quiz/<int:quiz_id>/leaderboard/', views.leaderboard, name='leaderboard'),
    
    # 퀴즈 진행
    path('question/<uuid:session_id>/', views.question_view, name='question'),
    path('submit/<uuid:session_id>/', views.submit_answer, name='submit_answer'),
    path('next/<uuid:session_id>/', views.next_question, name='next_question'),
    path('complete/<uuid:session_id>/', views.complete_quiz, name='complete_quiz'),
    path('result/<uuid:session_id>/', views.result_view, name='result'),
] 