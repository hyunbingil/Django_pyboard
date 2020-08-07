from django.urls import path

from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:question_id>/', views.detail, name="detail"),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    # http://localhost:8000/pybo/<int:question_id>/ 가 적용되어
    # question_id 에 2라는 값이 저장되고 views.detail 함수가 실행
    path('question/create/', views.question_create, name="question_create"),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
]