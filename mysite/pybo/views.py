from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question

def index(request):
    """
    pybo 목록 출력
    """
    question_list = Question.objects.order_by('-create_date')
    # 질문 목록 데이터를 얻는다.
    # order_by는 조회 결과를 정렬하는 함수.
    # create_date를 작성 일시의 역순으로(-) 정렬하라.
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk = question_id)
    # 매개변수 question_id에는 URL 매핑시 저장된 question_id가 전달
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # POST로 전송된 폼 데이터 항목 중 content의 값을 의미.
    # 답변 생성을 하기 위해 question.asnswer_set.create 사용
    # question.answer_set은 질문의 답변을 의미한다.
    # => ForeignKey로 연결 되어있기 때문에 이처럼 사용 가능.
    return redirect('pybo:detail', question_id=question.id)
    # 답변 생성 후 상세 조회 화면 호출을 위해 redirect 사용.
    # question_id는 다음과 같이 정의된 URL매핑에 question_id 를 전달하기 위해 필요하다.


    # Answer 모델을 직접 사용하는 방법
    # question = get_object_or_404(Question, pk=question_id)
    # answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    # answer.save()