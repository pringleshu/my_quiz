from django.core.management.base import BaseCommand
from django.db import transaction
from quiz.models import Quiz, Question, Choice, QuizStats

class Command(BaseCommand):
    help = '샘플 퀴즈 데이터를 생성합니다'

    def handle(self, *args, **options):
        self.stdout.write('샘플 퀴즈 데이터를 생성하는 중...')
        
        with transaction.atomic():
            # 기존 데이터 삭제 (선택사항)
            # Quiz.objects.all().delete()
            
            # 첫 번째 퀴즈: 나에 대한 퀴즈
            quiz1 = Quiz.objects.create(
                title="나를 얼마나 알고 있을까? 🤔",
                description="친구들이 나에 대해 얼마나 잘 알고 있는지 확인해보는 퀴즈입니다!",
                is_active=True
            )
            
            # 질문 1
            q1 = Question.objects.create(
                quiz=quiz1,
                text="내가 가장 좋아하는 음식은?",
                order=1
            )
            Choice.objects.create(question=q1, text="피자", is_correct=True, order=1)
            Choice.objects.create(question=q1, text="치킨", is_correct=False, order=2)
            Choice.objects.create(question=q1, text="햄버거", is_correct=False, order=3)
            Choice.objects.create(question=q1, text="초밥", is_correct=False, order=4)
            
            # 질문 2
            q2 = Question.objects.create(
                quiz=quiz1,
                text="내가 가장 좋아하는 색깔은?",
                order=2
            )
            Choice.objects.create(question=q2, text="빨간색", is_correct=False, order=1)
            Choice.objects.create(question=q2, text="파란색", is_correct=True, order=2)
            Choice.objects.create(question=q2, text="노란색", is_correct=False, order=3)
            Choice.objects.create(question=q2, text="초록색", is_correct=False, order=4)
            
            # 질문 3
            q3 = Question.objects.create(
                quiz=quiz1,
                text="내가 가장 자주 하는 취미는?",
                order=3
            )
            Choice.objects.create(question=q3, text="게임하기", is_correct=True, order=1)
            Choice.objects.create(question=q3, text="영화보기", is_correct=False, order=2)
            Choice.objects.create(question=q3, text="독서하기", is_correct=False, order=3)
            Choice.objects.create(question=q3, text="운동하기", is_correct=False, order=4)
            
            # 질문 4
            q4 = Question.objects.create(
                quiz=quiz1,
                text="내가 가장 무서워하는 것은?",
                order=4
            )
            Choice.objects.create(question=q4, text="거미", is_correct=False, order=1)
            Choice.objects.create(question=q4, text="높은 곳", is_correct=True, order=2)
            Choice.objects.create(question=q4, text="어둠", is_correct=False, order=3)
            Choice.objects.create(question=q4, text="벌레", is_correct=False, order=4)
            
            # 질문 5
            q5 = Question.objects.create(
                quiz=quiz1,
                text="내가 가장 좋아하는 계절은?",
                order=5
            )
            Choice.objects.create(question=q5, text="봄", is_correct=False, order=1)
            Choice.objects.create(question=q5, text="여름", is_correct=False, order=2)
            Choice.objects.create(question=q5, text="가을", is_correct=True, order=3)
            Choice.objects.create(question=q5, text="겨울", is_correct=False, order=4)
            
            # 퀴즈 통계 초기화
            QuizStats.objects.create(quiz=quiz1)
            
            # 두 번째 퀴즈: 일반 상식 퀴즈
            quiz2 = Quiz.objects.create(
                title="간단한 상식 퀴즈 🧠",
                description="기본적인 상식을 테스트하는 재미있는 퀴즈입니다!",
                is_active=True
            )
            
            # 질문 1
            q1 = Question.objects.create(
                quiz=quiz2,
                text="한국의 수도는?",
                order=1
            )
            Choice.objects.create(question=q1, text="부산", is_correct=False, order=1)
            Choice.objects.create(question=q1, text="서울", is_correct=True, order=2)
            Choice.objects.create(question=q1, text="대구", is_correct=False, order=3)
            Choice.objects.create(question=q1, text="인천", is_correct=False, order=4)
            
            # 질문 2
            q2 = Question.objects.create(
                quiz=quiz2,
                text="피자의 원산지는?",
                order=2
            )
            Choice.objects.create(question=q2, text="프랑스", is_correct=False, order=1)
            Choice.objects.create(question=q2, text="스페인", is_correct=False, order=2)
            Choice.objects.create(question=q2, text="이탈리아", is_correct=True, order=3)
            Choice.objects.create(question=q2, text="그리스", is_correct=False, order=4)
            
            # 질문 3
            q3 = Question.objects.create(
                quiz=quiz2,
                text="지구에서 가장 큰 바다는?",
                order=3
            )
            Choice.objects.create(question=q3, text="대서양", is_correct=False, order=1)
            Choice.objects.create(question=q3, text="태평양", is_correct=True, order=2)
            Choice.objects.create(question=q3, text="인도양", is_correct=False, order=3)
            Choice.objects.create(question=q3, text="북극해", is_correct=False, order=4)
            
            # 퀴즈 통계 초기화
            QuizStats.objects.create(quiz=quiz2)
            
            # 세 번째 퀴즈: 재미있는 퀴즈
            quiz3 = Quiz.objects.create(
                title="이것만 알면 당신은 천재! 🌟",
                description="조금 어렵지만 재미있는 퀴즈들을 모았습니다!",
                is_active=True
            )
            
            # 질문 1
            q1 = Question.objects.create(
                quiz=quiz3,
                text="다음 중 가장 가벼운 것은?",
                order=1
            )
            Choice.objects.create(question=q1, text="1kg의 철", is_correct=False, order=1)
            Choice.objects.create(question=q1, text="1kg의 솜", is_correct=False, order=2)
            Choice.objects.create(question=q1, text="1kg의 깃털", is_correct=False, order=3)
            Choice.objects.create(question=q1, text="모두 같다", is_correct=True, order=4)
            
            # 질문 2
            q2 = Question.objects.create(
                quiz=quiz3,
                text="바나나는 원래 무슨 색이었을까요?",
                order=2
            )
            Choice.objects.create(question=q2, text="노란색", is_correct=False, order=1)
            Choice.objects.create(question=q2, text="초록색", is_correct=True, order=2)
            Choice.objects.create(question=q2, text="빨간색", is_correct=False, order=3)
            Choice.objects.create(question=q2, text="보라색", is_correct=False, order=4)
            
            # 퀴즈 통계 초기화
            QuizStats.objects.create(quiz=quiz3)
        
        self.stdout.write(
            self.style.SUCCESS('✅ 샘플 퀴즈 데이터가 성공적으로 생성되었습니다!')
        )
        self.stdout.write('생성된 퀴즈:')
        self.stdout.write('  1. 나를 얼마나 알고 있을까? (5문제)')
        self.stdout.write('  2. 간단한 상식 퀴즈 (3문제)')
        self.stdout.write('  3. 이것만 알면 당신은 천재! (2문제)')
        self.stdout.write('')
        self.stdout.write('🚀 이제 개발 서버를 실행하고 http://127.0.0.1:8000 으로 접속해보세요!')
        self.stdout.write('👤 관리자 패널: http://127.0.0.1:8000/admin (계정: admin)') 