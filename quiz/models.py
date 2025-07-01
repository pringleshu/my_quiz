from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Quiz(models.Model):
    """퀴즈 세션을 관리하는 모델"""
    title = models.CharField(max_length=200, verbose_name="퀴즈 제목")
    description = models.TextField(blank=True, verbose_name="설명")
    is_active = models.BooleanField(default=True, verbose_name="활성화")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "퀴즈"
        verbose_name_plural = "퀴즈 목록"
    
    def __str__(self):
        return self.title

class Question(models.Model):
    """질문을 관리하는 모델"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name="질문 내용")
    order = models.PositiveIntegerField(default=0, verbose_name="질문 순서")
    is_active = models.BooleanField(default=True, verbose_name="활성화")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "질문"
        verbose_name_plural = "질문 목록"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"

class Choice(models.Model):
    """선택지를 관리하는 모델"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200, verbose_name="선택지 내용")
    is_correct = models.BooleanField(default=False, verbose_name="정답 여부")
    order = models.PositiveIntegerField(default=0, verbose_name="선택지 순서")
    
    class Meta:
        verbose_name = "선택지"
        verbose_name_plural = "선택지 목록"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.question.text[:30]} - {self.text}"

class UserSession(models.Model):
    """사용자 세션을 관리하는 모델 (익명 사용자 지원)"""
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nickname = models.CharField(max_length=50, verbose_name="닉네임")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='user_sessions')
    current_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    is_completed = models.BooleanField(default=False, verbose_name="완료 여부")
    score = models.IntegerField(default=0, verbose_name="점수")
    total_questions = models.IntegerField(default=0, verbose_name="총 문제 수")
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "사용자 세션"
        verbose_name_plural = "사용자 세션 목록"
    
    def __str__(self):
        return f"{self.nickname} - {self.quiz.title}"
    
    @property
    def completion_percentage(self):
        if self.total_questions == 0:
            return 0
        return (self.score / self.total_questions) * 100

class UserAnswer(models.Model):
    """사용자 답변을 기록하는 모델"""
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False, verbose_name="정답 여부")
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "사용자 답변"
        verbose_name_plural = "사용자 답변 목록"
        unique_together = ['session', 'question']
    
    def save(self, *args, **kwargs):
        # 정답 여부 자동 판정
        self.is_correct = self.selected_choice.is_correct
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.session.nickname} - {self.question.text[:30]}"

class QuizStats(models.Model):
    """퀴즈 통계를 관리하는 모델"""
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE, related_name='stats')
    total_attempts = models.IntegerField(default=0, verbose_name="총 시도 횟수")
    total_completions = models.IntegerField(default=0, verbose_name="총 완료 횟수")
    average_score = models.FloatField(default=0.0, verbose_name="평균 점수")
    highest_score = models.IntegerField(default=0, verbose_name="최고 점수")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "퀴즈 통계"
        verbose_name_plural = "퀴즈 통계 목록"
    
    def __str__(self):
        return f"{self.quiz.title} 통계"
