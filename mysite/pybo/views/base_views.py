from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from ..models import Question

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