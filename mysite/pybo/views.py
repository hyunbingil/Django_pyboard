from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator

def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1') # 페이지
    # page값이 없을 경우에는 디폴트로 1이라는 값을 설정
    
    # 조회
    question_list = Question.objects.order_by('-create_date')
    # 질문 목록 데이터를 얻는다.
    # order_by는 조회 결과를 정렬하는 함수.
    # create_date를 작성 일시의 역순으로(-) 정렬하라.

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
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
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

def question_create(request):
    """
    pybo 질문등록
    """
    if request.method == 'POST': # 저장하기 버튼 클릭 시 post 방식으로 호출된다.
        # 데이터 저장
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            # 폼에 연결된 모델을 저장하지 않고 생성된 모델 객체만 리턴(commit=False)
            # 코드내에서 자동으로 생성되는 값을 저장하기 위해서는 이것을 사용해야함.
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else: # 질문 등록하기 버튼 클릭했을 경우 get 방식으로 호출된다.
        # 질문등록 화면 호출
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)