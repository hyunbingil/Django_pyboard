## URL 분리
: pybo앱에 속한 것들은 대부분 pybo앱 디렉터리 하위에 위치해야하는데, pybo앱에 기능을 추가할 때마다 ```urls.py``` 파일을 수정해야 한다.\
=> ```urls.py``` 파일에는 pybo앱 뿐만 아니라 다른 앱의 내용도 추가되어야 하기 때문에\
==> pybo앱에서 사용하는 URL들을 ```urls.py``` 파일에 계속 추가하는 것은 좋지 않을 것이다.
``` py
from django.contrib import admin
from django.urls import path
from pybo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')), # 뒤에 / 붙여주기
]
```
: ```path('pybo/', include('pybo.urls'))```의 의미는 ```pybo/``` 로 시작되는 URL이 요청되면\
이제 ```pybo/urls.py``` 파일의 매핑정보를 읽어서 처리하라는 의미이다.\
=> 따라서 이제 ```pybo/question/create```, ```pybo/answer/create```등의 URL이 추가되더라도\
```config/urls.py``` 파일을 수정할 필요없이 ```pybo/urls.py``` 파일만 수정하면 될것이다.

---

## 모델(Model)
: 장고는 모델(Model)을 이용하여 데이터베이스를 처리한다.\
보통 데이터베이스에 데이터를 저장하고 조회하기 위해서 SQL 쿼리문을 이용해야 하지만\
장고의 모델(Model)을 사용하면 이런 SQL 쿼리문의 도움없이 데이터를 쉽게 처리할 수 있다.

### settings.py
: 앱들의 정보와 데이터베이스에 대한 정보도 정의되어 있음.
``` py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), # BASE_DIR은 프로젝트 디렉터리를 의미한다. (※ 우리의 BASE_DIR은 ~~mysite 이다.)
    }
}
```

## 모델 만들기
### 모델의 속성
1. 질문(Question) 모델
```
속성명	설명
subject	질문의 제목
content	질문의 내용
create_date	질문을 작성한 일시
```
2. 답변(Answer) 모델
```
속성명	설명
question	질문 (어떤 질문의 답변인지 알아야하므로 질문 속성이 필요하다.)
content	답변의 내용
create_date	답변을 작성한 일시
```

### ```models.py```
``` py
from django.db import models

# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200) # 제목 : 최대 200자 / 글자 수 제한 O(CharField)
    content = models.TextField() # 내용 : 글자 수 제한 X(TextField)
    create_date = models.DateTimeField() # 작성 일시 : 날짜와 시간에 관계된 속성(DateTimeField)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # 질문에 대한 답변에 해당되므로 Question 모델을 속성으로 가져가야 한다.
    # on_delete=models.CASCADE의 의미는
    # 이 답변과 연결된 질문(Question)이 삭제될 경우 답변(Answer)도 함께 삭제된다는 의미.
    content = models.TextField()
    create_date = models.DateTimeField()
```
- 장고에서 사용하는 속성(Field)의 타입 참고 링크\
https://docs.djangoproject.com/en/3.0/ref/models/fields/#field-types

### makemigrations
: 모델이 변경되면 이 명령을 먼저 수행하고 migrate 명령을 수행해야 한다.
```
python manage.py makemigrations
```

### migrate
: 실제 테이블 생성
```
python manage.py migrate
```

### sqlmigrate
: migrate 실행시 실제 어떤 쿼리문이 실행되는지는 sqlmigrate 명령을 이용하여 확인할 수 있다.
```
(mysite) C:\projects\mysite>python manage.py sqlmigrate pybo 0001
BEGIN;
--
-- Create model Question
--
CREATE TABLE "pybo_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "subject" varchar(200) NOT NULL, "content" text NOT NULL, "create_date" datetime NOT NULL);
--
-- Create model Answer
--
CREATE TABLE "pybo_answer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content" text NOT NULL, "create_date" datetime NOT NULL, "question_id" integer NOT NULL REFERENCES "pybo_question" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "pybo_answer_question_id_e174c39f" ON "pybo_answer" ("question_id");
COMMIT;

(mysite) C:\projects\mysite> 
```
> python manage.py sqlmigrate pybo 0001 명령에서 "pybo"는 makemigrations 명렁어 수행시 생성되었던 pybo\migrations\0001_initial.py 파일의 마이그레이션명 'pybo'를 의미하고 "0001"은 생성된 파일의 일련번호를 의미한다.

### shell 이용해서 model 만들기

---

## 슈퍼 유저
```
python manage.py createsuperuser
```
### 모델 관리
: 앱 디렉터리에 admin.py 파일에 만든 model을 넣어보자
``` py
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```

### 모델 검색
: 제목 검색을 해보자.
``` py
from django.contrib import admin
from .models import Question
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']
# model 검색하기

admin.site.register(Question, QuestionAdmin)
```

---

## 템플릿 디렉터리
### 1. ```settings.py``` 파일의 TEMPLATES 항목에 추가하기
``` py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
            # BASE_DIR는 mysite이다.
            # DIRS에 설정한 디렉터리 외에도 앱(App) 디렉터리 하위에 있는 templates 디렉터리도 템플릿 디렉터리로 인식함.
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
- 공통 템플릿 디렉터리 - ```./mysite/mysite/templates```
- 파이보 앱 템플릿 디렉터리 - ```./mysite/templates/pybo```

### 2. 템플릿 파일 만들기
``` html
{% if question_list %}
    <ul>
    {% for question in question_list %}
        <li><a href="/pybo/{{ question.id }}/">{{ question.subject }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>질문이 없습니다.</p>
{% endif %}
```
### 🍯 템플릿 태그
: ```{%``` 와 ```%}``` 로 둘러싸인 문장들
#### 1) 분기
: 파이썬 if 문과 다른 게 없지만, 마지막에 ```{% endif %}```태그로 닫아주어야 함.
``` html
{% if 조건문1 %}
    <p>조건문1에 해당되는 경우</p>
{% elif 조건문2 %}
    <p>조건문2에 해당되는 경우</p>
{% else %}
    <p>조건문1, 2에 모두 해당되지 않는 경우</p>
{% endif %}
```
#### 2) 반복
: 마지막은 항상 {% endfor %} 태그로 닫아주어야 한다.
``` html
{% for item in list %}
    <p>순서: {{ forloop.counter }} </p>
    <p>{{ item }}</p>
{% endfor %}
```
- forloop.counter : 루프내의 순서로 1부터 표시
- forloop.counter0 : 루프내의 순서로 0부터 표시
- forloop.first : 루프의 첫번째 순서인 경우 True
- forloop.last : 루프의 마지막 순서인 경우 True

#### 3) 객체 출력
: 객체에 속성이 있는 경우는 파이썬과 동일한 방법으로 도트(.) 문자를 이용하여 표시하면 된다.
``` html
{{ 객체 }} <!--객체 출력-->
{{ 객체.속성 }} <!--속성이 있는 경우-->
```
