from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import F, Avg
from django.contrib import messages
import json

from .models import Quiz, Question, Choice, UserSession, UserAnswer, QuizStats

def home(request):
    """메인 페이지 - 활성화된 퀴즈 목록 표시"""
    active_quizzes = Quiz.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'quizzes': active_quizzes,
        'total_quizzes': active_quizzes.count(),
    }
    return render(request, 'quiz/home.html', context)

def quiz_detail(request, quiz_id):
    """퀴즈 상세 정보 및 시작 페이지"""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    question_count = quiz.questions.filter(is_active=True).count()
    
    # 퀴즈 통계 가져오기 또는 생성
    stats, created = QuizStats.objects.get_or_create(quiz=quiz)
    
    context = {
        'quiz': quiz,
        'question_count': question_count,
        'stats': stats,
    }
    return render(request, 'quiz/quiz_detail.html', context)

def start_quiz(request, quiz_id):
    """퀴즈 시작 - 닉네임 입력 후 세션 생성"""
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
        nickname = request.POST.get('nickname', '').strip()
        
        if not nickname:
            messages.error(request, '닉네임을 입력해주세요.')
            return redirect('quiz:quiz_detail', quiz_id=quiz_id)
        
        if len(nickname) > 50:
            messages.error(request, '닉네임은 50자 이하로 입력해주세요.')
            return redirect('quiz:quiz_detail', quiz_id=quiz_id)
        
        # 새 사용자 세션 생성
        questions = quiz.questions.filter(is_active=True).order_by('order')
        if not questions.exists():
            messages.error(request, '이 퀴즈에는 활성화된 질문이 없습니다.')
            return redirect('quiz:quiz_detail', quiz_id=quiz_id)
        
        user_session = UserSession.objects.create(
            nickname=nickname,
            quiz=quiz,
            current_question=questions.first(),
            total_questions=questions.count()
        )
        
        # 퀴즈 통계 업데이트
        stats, created = QuizStats.objects.get_or_create(quiz=quiz)
        stats.total_attempts = F('total_attempts') + 1
        stats.save()
        
        # 세션 ID를 쿠키에 저장
        response = redirect('quiz:question', session_id=user_session.session_id)
        response.set_cookie('quiz_session', str(user_session.session_id), max_age=3600*24)  # 24시간
        return response
    
    return redirect('quiz:quiz_detail', quiz_id=quiz_id)

def question_view(request, session_id):
    """질문 표시 및 답변 처리"""
    user_session = get_object_or_404(UserSession, session_id=session_id)
    
    if user_session.is_completed:
        return redirect('quiz:result', session_id=session_id)
    
    current_question = user_session.current_question
    if not current_question:
        # 다음 질문 찾기
        answered_questions = user_session.answers.values_list('question_id', flat=True)
        next_question = user_session.quiz.questions.filter(
            is_active=True
        ).exclude(id__in=answered_questions).order_by('order').first()
        
        if next_question:
            user_session.current_question = next_question
            user_session.save()
            current_question = next_question
        else:
            # 모든 질문 완료
            return redirect('quiz:complete_quiz', session_id=session_id)
    
    # 이전 답변 확인
    try:
        previous_answer = UserAnswer.objects.get(
            session=user_session,
            question=current_question
        )
        # 이미 답변한 질문이면 다음 질문으로
        return redirect('quiz:next_question', session_id=session_id)
    except UserAnswer.DoesNotExist:
        pass
    
    # 진행률 계산
    answered_count = user_session.answers.count()
    progress_percentage = (answered_count / user_session.total_questions) * 100 if user_session.total_questions > 0 else 0
    
    context = {
        'user_session': user_session,
        'question': current_question,
        'choices': current_question.choices.all().order_by('order'),
        'question_number': answered_count + 1,
        'total_questions': user_session.total_questions,
        'progress_percentage': progress_percentage,
    }
    return render(request, 'quiz/question.html', context)

@csrf_exempt
def submit_answer(request, session_id):
    """답변 제출 처리 (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)
    
    user_session = get_object_or_404(UserSession, session_id=session_id)
    
    if user_session.is_completed:
        return JsonResponse({'error': '이미 완료된 퀴즈입니다.'}, status=400)
    
    try:
        data = json.loads(request.body)
        choice_id = data.get('choice_id')
        
        if not choice_id:
            return JsonResponse({'error': '선택지를 선택해주세요.'}, status=400)
        
        choice = get_object_or_404(Choice, id=choice_id)
        current_question = user_session.current_question
        
        if choice.question != current_question:
            return JsonResponse({'error': '잘못된 선택지입니다.'}, status=400)
        
        # 이미 답변했는지 확인
        if UserAnswer.objects.filter(session=user_session, question=current_question).exists():
            return JsonResponse({'error': '이미 답변한 질문입니다.'}, status=400)
        
        # 답변 저장
        user_answer = UserAnswer.objects.create(
            session=user_session,
            question=current_question,
            selected_choice=choice
        )
        
        # 점수 업데이트
        if user_answer.is_correct:
            user_session.score = F('score') + 1
            user_session.save()
            user_session.refresh_from_db()
        
        # 다음 질문 찾기
        answered_questions = user_session.answers.values_list('question_id', flat=True)
        next_question = user_session.quiz.questions.filter(
            is_active=True
        ).exclude(id__in=answered_questions).order_by('order').first()
        
        if next_question:
            user_session.current_question = next_question
            user_session.save()
            next_url = f"/question/{session_id}/"
        else:
            # 퀴즈 완료
            user_session.is_completed = True
            user_session.completed_at = timezone.now()
            user_session.current_question = None
            user_session.save()
            
            # 통계 업데이트
            update_quiz_stats(user_session.quiz)
            
            next_url = f"/result/{session_id}/"
        
        return JsonResponse({
            'success': True,
            'is_correct': user_answer.is_correct,
            'correct_answer': choice.question.choices.filter(is_correct=True).first().text,
            'next_url': next_url,
            'score': user_session.score,
            'total_questions': user_session.total_questions
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': '잘못된 데이터 형식입니다.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': '서버 오류가 발생했습니다.'}, status=500)

def next_question(request, session_id):
    """다음 질문으로 이동"""
    user_session = get_object_or_404(UserSession, session_id=session_id)
    
    if user_session.is_completed:
        return redirect('quiz:result', session_id=session_id)
    
    # 다음 질문 찾기
    answered_questions = user_session.answers.values_list('question_id', flat=True)
    next_question = user_session.quiz.questions.filter(
        is_active=True
    ).exclude(id__in=answered_questions).order_by('order').first()
    
    if next_question:
        user_session.current_question = next_question
        user_session.save()
        return redirect('quiz:question', session_id=session_id)
    else:
        return redirect('quiz:complete_quiz', session_id=session_id)

def complete_quiz(request, session_id):
    """퀴즈 완료 처리"""
    user_session = get_object_or_404(UserSession, session_id=session_id)
    
    if not user_session.is_completed:
        user_session.is_completed = True
        user_session.completed_at = timezone.now()
        user_session.current_question = None
        user_session.save()
        
        # 통계 업데이트
        update_quiz_stats(user_session.quiz)
    
    return redirect('quiz:result', session_id=session_id)

def result_view(request, session_id):
    """퀴즈 결과 표시"""
    user_session = get_object_or_404(UserSession, session_id=session_id)
    
    if not user_session.is_completed:
        return redirect('quiz:question', session_id=session_id)
    
    # 결과 분석
    total_questions = user_session.total_questions
    correct_answers = user_session.score
    percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # 랭킹 계산 (같은 퀴즈의 다른 참여자들과 비교)
    better_scores = UserSession.objects.filter(
        quiz=user_session.quiz,
        is_completed=True,
        score__gt=user_session.score
    ).count()
    
    total_participants = UserSession.objects.filter(
        quiz=user_session.quiz,
        is_completed=True
    ).count()
    
    rank = better_scores + 1
    
    # 상세 답변 내역
    answers = user_session.answers.select_related(
        'question', 'selected_choice'
    ).order_by('question__order')
    
    context = {
        'user_session': user_session,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'percentage': percentage,
        'rank': rank,
        'total_participants': total_participants,
        'answers': answers,
    }
    return render(request, 'quiz/result.html', context)

def leaderboard(request, quiz_id):
    """퀴즈 리더보드"""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    
    # 상위 10명의 결과
    top_sessions = UserSession.objects.filter(
        quiz=quiz,
        is_completed=True
    ).order_by('-score', 'completed_at')[:10]
    
    # 통계
    stats, created = QuizStats.objects.get_or_create(quiz=quiz)
    
    context = {
        'quiz': quiz,
        'top_sessions': top_sessions,
        'stats': stats,
    }
    return render(request, 'quiz/leaderboard.html', context)

def update_quiz_stats(quiz):
    """퀴즈 통계 업데이트"""
    stats, created = QuizStats.objects.get_or_create(quiz=quiz)
    
    completed_sessions = UserSession.objects.filter(quiz=quiz, is_completed=True)
    
    stats.total_completions = completed_sessions.count()
    if stats.total_completions > 0:
        stats.average_score = completed_sessions.aggregate(avg_score=Avg('score'))['avg_score'] or 0
        stats.highest_score = completed_sessions.order_by('-score').first().score
    
    stats.save()
