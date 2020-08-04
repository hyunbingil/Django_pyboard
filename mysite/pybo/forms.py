from django import forms
from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta: # 내부 클래스 Meta
        model = Question # Question이라는 모델과 연결된 폼
        fields = ['subject', 'content'] # 속성
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        # }
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }