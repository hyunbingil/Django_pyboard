from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200) # 제목 : 최대 200자 / 글자 수 제한 O(CharField)
    content = models.TextField() # 내용 : 글자 수 제한 X(TextField)
    create_date = models.DateTimeField() # 작성 일시 : 날짜와 시간에 관계된 속성(DateTimeField)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 저자
    modify_date = models.DateTimeField(null=True, blank=True) # 수정 일시
    # django.contrib.auth.models 패키지의 User이므로 글쓴이에 해당되는 author 속성은 User모델을 ForeignKey로 적용해야 한다.
    def __str__(self):
        return self.subject

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # 질문에 대한 답변에 해당되므로 Question 모델을 속성으로 가져가야 한다.
    # on_delete=models.CASCADE의 의미는
    # 이 답변과 연결된 질문(Question)이 삭제될 경우 답변(Answer)도 함께 삭제된다는 의미.
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    modify_date = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.subject