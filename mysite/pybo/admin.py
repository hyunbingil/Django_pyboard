from django.contrib import admin
from .models import Question
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']
# model 검색하기

admin.site.register(Question, QuestionAdmin)