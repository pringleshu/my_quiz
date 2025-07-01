from django.contrib import admin
from .models import Quiz, Question, Choice, UserSession, UserAnswer, QuizStats

class ChoiceInline(admin.TabularInline):
    """질문 편집 시 선택지를 인라인으로 표시"""
    model = Choice
    extra = 4  # 기본적으로 4개의 빈 선택지 제공
    fields = ['text', 'is_correct', 'order']

class QuestionInline(admin.TabularInline):
    """퀴즈 편집 시 질문을 인라인으로 표시"""
    model = Question
    extra = 1
    fields = ['text', 'order', 'is_active']
    show_change_link = True

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at', 'question_count', 'attempt_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    inlines = [QuestionInline]
    readonly_fields = ['created_at', 'updated_at']
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = '질문 수'
    
    def attempt_count(self, obj):
        return obj.user_sessions.count()
    attempt_count.short_description = '시도 횟수'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'quiz', 'order', 'is_active', 'choice_count']
    list_filter = ['quiz', 'is_active', 'created_at']
    search_fields = ['text', 'quiz__title']
    inlines = [ChoiceInline]
    list_editable = ['order', 'is_active']
    ordering = ['quiz', 'order']
    
    def text_preview(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_preview.short_description = '질문 내용'
    
    def choice_count(self, obj):
        return obj.choices.count()
    choice_count.short_description = '선택지 수'

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'question_preview', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['text', 'question__text']
    list_editable = ['is_correct', 'order']
    ordering = ['question__quiz', 'question__order', 'order']
    
    def question_preview(self, obj):
        return obj.question.text[:50] + '...' if len(obj.question.text) > 50 else obj.question.text
    question_preview.short_description = '질문'

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'quiz', 'score', 'total_questions', 'completion_percentage_display', 'is_completed', 'started_at']
    list_filter = ['quiz', 'is_completed', 'started_at']
    search_fields = ['nickname', 'quiz__title']
    readonly_fields = ['session_id', 'started_at', 'completed_at', 'completion_percentage']
    ordering = ['-started_at']
    
    def completion_percentage_display(self, obj):
        return f"{obj.completion_percentage:.1f}%"
    completion_percentage_display.short_description = '완료율'

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['session_nickname', 'question_preview', 'selected_choice', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'answered_at', 'question__quiz']
    search_fields = ['session__nickname', 'question__text']
    readonly_fields = ['answered_at']
    ordering = ['-answered_at']
    
    def session_nickname(self, obj):
        return obj.session.nickname
    session_nickname.short_description = '사용자'
    
    def question_preview(self, obj):
        return obj.question.text[:50] + '...' if len(obj.question.text) > 50 else obj.question.text
    question_preview.short_description = '질문'

@admin.register(QuizStats)
class QuizStatsAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'total_attempts', 'total_completions', 'completion_rate', 'average_score', 'highest_score']
    readonly_fields = ['quiz', 'total_attempts', 'total_completions', 'average_score', 'highest_score', 'updated_at']
    
    def completion_rate(self, obj):
        if obj.total_attempts == 0:
            return "0%"
        return f"{(obj.total_completions / obj.total_attempts * 100):.1f}%"
    completion_rate.short_description = '완료율'
    
    def has_add_permission(self, request):
        return False  # 통계는 자동 생성되므로 추가 금지
    
    def has_delete_permission(self, request, obj=None):
        return False  # 통계 삭제 금지

# 관리자 사이트 설정
admin.site.site_header = "나 몰라 퀴즈 관리"
admin.site.site_title = "퀴즈 관리"
admin.site.index_title = "퀴즈 관리 시스템"
