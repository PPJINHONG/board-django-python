
from django import template



register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg


# #템플릿 필터 함수 만드는방법  #@register.filter 애너테이션 적용하면 해당 함수를 필터로 사용가능
# 사용시 {# load pybo_filter #} 선언 후 사용 객체.값|함수

# EX= #list.paginator.count|sub:list.start_index|sub:forloop.counter0|add:1
#    번 호 = 전 체 건 수 - 시 작 인 덱 스 - 현 재 인 덱 스 + 1 -

