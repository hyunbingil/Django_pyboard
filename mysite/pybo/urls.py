from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('<int:question_id>/', views.detail),
    # http://localhost:8000/pybo/<int:question_id>/ 가 적용되어
    # question_id 에 2라는 값이 저장되고 views.detail 함수가 실행
]