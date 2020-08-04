## 데이터 저장
### ```{% csrf_token %}```
: 보안에 관련된 항목으로 form으로 전송된 데이터가 실제 웹페이지에서 작성된 데이터인지를 판단해 주는 가늠자 역할.\
: 기타 다른 해킹 툴등에 의해서 데이터가 전송될 경우에는 서버에서 발행한 csrf_token값과 해당 툴에서 보낸 csrf_token 값이 일치하지 않기때문에 오류가 발생한다.\
=> 따라서 form태그 바로 밑에 ```{% csrf_token %}``` 을 항상 위치시키도록 해야 한다.

---

## 스태틱
### static 디렉터리
: 스타일시트 파일은 장고의 스태틱 디렉터리에 저장해야 한다.\
: 스태틱 디렉터리도 템플릿 디렉터리와 마찬가지로 config/settings.py 파일에 등록해 주어야 한다. 
``` py
...
STATIC_URL = '/static/'
# ---------------------------------------- [edit] ---------------------------------------- #
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# ---------------------------------------------------------------------------------------- #
```
### 스타일시트
: static 디렉터리 안에 넣어야한다.
> 스태틱(static) 파일이란 주로 이미지(png, jpg)나 자바스크립트(js), 스타일시트(css)와 같은 파일을 의미한다.

### 템플릿에 스타일 적용
: 스타일시트와 같은 스태틱파일을 사용하기 위해서는 템플릿 가장 상단에 ```{% load static %}``` 태그를 삽입해야 한다. 그리고 스타일시트 파일 경로는 ```{% static 'style.css' %}``` 처럼 사용하였다.
``` html
{% load static %}
<link rel="stylesheet" type="text/css" href="{% static 'style.css' %}">
```

---

## 템플릿 상속
: 표준 HTML구조가 되도록 템플릿을 수정해 보자.\
: 하지만 모든 템플릿이 <body> 태그 바깥 부분은 모두 동일한 내용으로 중복될 것이다.\
: 그리고 스타일시트 명이 변경되거나 새로운 스타일시트가 추가될 경우에도 모든 템플릿을 수정해 주어야 하는 불편함도 발생할 것이다.\
=> __이런 중복과 불편함을 없애기 위해 템플릿을 상속(extend)해서 사용할수 있는 방법을 지원.__

### ```base.html```
: ```base.html 템플릿```은 모든 템플릿이 상속해야 하는 템플릿으로 표준 HTML문서의 기본 틀이된다.\
: body 태그 안의 ```{% block content %}``` 와 ```{% endblock %}``` 는 ```base.html```을 상속한 템플릿에서 구현해야 하는 영역이 된다.
``` html
{% load static %}
<!doctype html>
<html lang="ko">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" type="text/css" href="{% static 'bootstrap.min.css' %}">
    <!-- pybo CSS -->
    <link rel="stylesheet" type="text/css" href="{% static 'style.css' %}">
    <title>Hello, pybo!</title>
</head>
<body>
<!-- 기본 템플릿 안에 삽입될 내용 Start -->
{% block content %}
{% endblock %}
<!-- 기본 템플릿 안에 삽입될 내용 End -->
</body>
</html>
```

### 상속받을 템플릿
: 플릿을 상속하기 위해서는 ```{% extends 'base.html' %}``` 처럼 ```extends 템플릿 문법```을 사용해야 한다.\
: ```{% block content %}``` 와 ```{% endblock %}``` 사이에 상속 받을 템플릿에서만 쓰이는 내용을 작성한다.
``` html
{% extends 'base.html' %}
{% block content %}

내용

{% endblock %}
```

---

## 폼
### 뷰 함수
: question_create함수는 QuestionForm을 사용한다.\
: QuestionForm은 질문을 등록하기 위해 사용할 장고 폼(Form)이다.
``` py
# ---------------------------------------- [edit] ---------------------------------------- #
from .forms import QuestionForm
# ---------------------------------------------------------------------------------------- #
...
# ---------------------------------------- [edit] ---------------------------------------- #
def question_create(request):
    """
    pybo 질문등록
    """
    form = QuestionForm()
    return render(request, 'pybo/question_form.html', {'form': form})
# ---------------------------------------------------------------------------------------- #
```
### 폼 작성
``` py
from django import forms
from pybo.models import Question


class QuestionForm(forms.ModelForm):
    class Meta: # 내부 클래스 Meta
        model = Question
        fields = ['subject', 'content']
```
- 일반 폼(forms.Form)
- 모델 폼(forms.ModelForm)\
: 모델(Model)과 연결된 폼으로 폼을 저장하면 연결된 모델의 데이터를 저장할 수 있게 된다.\
: 모델 폼은 class Meta 라는 내부(Inner) 클래스가 반드시 필요하다. Meta 클래스에는 사용할 모델과 모델의 속성을 적어주어야 한다.

### 템플릿 작성
: ```{{ form.as_p }}```는 제목과 내용같은 폼 입력항목을 위한 HTML코드들을 자동으로 만들어 낸다.
``` py
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <h5 class="my-3 border-bottom pb-2">질문등록</h5>
    <form method="post" class="post-form my-3">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">저장하기</button>
    </form>
</div>
{% endblock %}
```

### GET과 POST
``` py
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
```

### 폼 위젯
: Meta클래스에 widgets 속성을 지정하면 폼 입력 항목에 부트스트랩의 클래스를 추가할 수 있다.
``` py
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
```

#### answer_create
``` py
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
```    