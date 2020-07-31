from django.shortcuts import render, get_object_or_404
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