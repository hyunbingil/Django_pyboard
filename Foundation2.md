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