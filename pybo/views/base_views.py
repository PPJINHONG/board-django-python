from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.shortcuts import render
from .. models import Question
from django.db.models import Q



def index(request):
    indexpage = request.GET.get('page', '1') #페이지
    kw = request.GET.get('kw', '') #검색어
    question_list = Question.objects.order_by('-create_date') #create_date 역순
    if kw:
        question_list=question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(answer__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()
    indexpaginator = Paginator(question_list,10)
    indexpage_obj = indexpaginator.get_page(indexpage)
    context = {'question_list': indexpage_obj , 'page':indexpage, 'kw':kw}
    return render(request, 'pybo/question_list.html',context)

def detail(request,question_id):
    question = get_object_or_404(Question, pk=question_id)           #404page표시
    #question = Question.objects.get(id=question_id)                  기존방식
    context = {'question':question}
    return render(request, 'pybo/question_detail.html',context)

