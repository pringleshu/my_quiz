# 나 몰라 퀴즈 🤔

아이폰 사파리에 최적화된 Django 기반 퀴즈 웹사이트입니다. 관리자가 질문과 답변을 설정하면, 사용자들이 퀴즈에 도전할 수 있습니다.

## ✨ 주요 기능

### 👤 사용자 기능
- **퀴즈 참여**: 닉네임만 입력하면 바로 참여 가능
- **실시간 피드백**: 답변 후 즉시 정답/오답 확인
- **진행률 표시**: 현재 진행 상황을 시각적으로 확인
- **결과 분석**: 상세한 점수 및 순위 확인
- **결과 공유**: 결과를 친구들과 공유
- **리더보드**: 다른 참가자들과 점수 비교

### 👨‍💼 관리자 기능
- **퀴즈 관리**: 퀴즈 생성, 수정, 삭제
- **질문 관리**: 질문과 선택지 관리
- **통계 확인**: 참여자 수, 평균 점수 등 통계
- **답변 분석**: 사용자들의 답변 패턴 분석

### 📱 아이폰 사파리 최적화
- **터치 친화적 UI**: 터치 피드백과 햅틱 지원
- **반응형 디자인**: 모바일 화면에 완벽 최적화
- **PWA 지원**: 홈 화면에 추가 가능
- **부드러운 애니메이션**: 자연스러운 전환 효과

## 🚀 설치 및 실행

### 1. 가상환경 활성화
```bash
source venv/bin/activate
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 마이그레이션
```bash
python manage.py migrate
```

### 4. 샘플 데이터 생성 (선택사항)
```bash
python manage.py create_sample_quiz
```

### 5. 개발 서버 실행
```bash
python manage.py runserver
```

## 📋 사용법

### 사용자
1. **http://127.0.0.1:8000** 접속
2. 원하는 퀴즈 선택
3. 닉네임 입력 후 퀴즈 시작
4. 질문에 답변하며 퀴즈 진행
5. 결과 확인 및 공유

### 관리자
1. **http://127.0.0.1:8000/admin** 접속
2. 관리자 계정으로 로그인
   - **아이디**: admin
   - **비밀번호**: admin123
3. 퀴즈, 질문, 선택지 관리
4. 통계 및 사용자 답변 확인

## 🏗️ 프로젝트 구조

```
noly/
├── quiz/                      # 퀴즈 앱
│   ├── models.py             # 데이터 모델
│   ├── views.py              # 뷰 함수
│   ├── admin.py              # 관리자 설정
│   ├── urls.py               # URL 패턴
│   ├── templates/quiz/       # 템플릿
│   └── management/commands/  # 관리 명령
├── noly_quiz/               # 프로젝트 설정
├── requirements.txt         # 의존성 목록
└── manage.py               # Django 관리 스크립트
```

## 🎯 핵심 모델

### Quiz (퀴즈)
- 제목, 설명, 활성화 상태
- 생성/수정 시간

### Question (질문)
- 질문 내용, 순서
- 퀴즈와 연결

### Choice (선택지)
- 선택지 내용, 정답 여부
- 질문과 연결

### UserSession (사용자 세션)
- 닉네임, 점수, 완료 상태
- 익명 사용자 지원

### UserAnswer (사용자 답변)
- 선택한 답변, 정답 여부
- 답변 시간 기록

## 🎨 디자인 특징

- **모던한 UI**: Tailwind CSS 기반
- **그라디언트**: 아름다운 색상 조합
- **이모지**: 친근하고 재미있는 느낌
- **애니메이션**: 부드러운 전환 효과
- **카드 디자인**: 깔끔한 정보 표시

## 🔧 추가 기능

### 부가 기능들
- **실시간 통계**: 퀴즈별 참여자 및 점수 통계
- **순위 시스템**: 참가자간 순위 비교
- **답변 분석**: 상세한 답변 내역 제공
- **결과 공유**: 웹 공유 API 지원
- **햅틱 피드백**: 터치 반응 향상

### 관리 편의성
- **인라인 편집**: 관련 데이터를 한 번에 편집
- **필터링**: 데이터를 쉽게 찾고 관리
- **검색 기능**: 키워드로 빠른 검색
- **읽기 전용 필드**: 중요 데이터 보호

## 🌟 사용 시나리오

1. **친구들과 재미있는 시간**: 서로에 대해 얼마나 알고 있는지 테스트
2. **교육용 퀴즈**: 학습 내용을 퀴즈로 복습
3. **이벤트 활동**: 파티나 모임에서 재미있는 활동
4. **아이스브레이킹**: 새로운 사람들과 친해지기

## 📱 배포 준비

배포 전 체크리스트:
- [ ] `DEBUG = False` 설정
- [ ] `ALLOWED_HOSTS` 설정
- [ ] 정적 파일 설정
- [ ] 데이터베이스 설정
- [ ] 비밀키 보안

## 🤝 기여하기

1. 이슈 리포트
2. 기능 제안
3. 버그 수정
4. 문서화 개선

---

**즐거운 퀴즈 시간 되세요! 🎉** 