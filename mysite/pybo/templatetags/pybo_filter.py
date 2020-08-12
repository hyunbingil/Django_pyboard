import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def sub(value, arg):
    return value - arg

@register.filter()
def mark(value): # markdown 모듈과 mark_safe 함수를 이용해 입력된 문자열을 HTML 코드로 변환해주는 필터함수.
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))    