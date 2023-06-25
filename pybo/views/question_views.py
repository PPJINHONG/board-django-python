from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':  #3. 아래 질문등록버튼클릭후 들어오면 폼에 입력값을넣고 submit(POST)호출하면 여기로실행
        form = QuestionForm(request.POST) #4. request.POST를 인수로 QuestionForm 을 생성할 경우에는 request.POST에 담긴 subject,
                                           #  content 값이 QuestionForm 의 subject, content 속성에 자동으로 저장되어 객체가 생성.
        if form.is_valid():
            question = form.save(commit=False) #5. 임시 저장 question 객체를 리턴
            question.author = request.user # 로그인사용자 저장
            question.create_date = timezone.now()   ##6. 시간저장 //임시저장안하면 createdate값이없어서 오류발생
            question.save() # 7. 진짜 저장
            print(request.user) #사용자 이름
            return redirect('pybo:index') # 8. 리스트홈페이지 이동

    else:   # 1. 처음 기본 list페이지 질문등록버튼클릭시 default값을 GET방식 호출 기본 폼만 리다이렉됨
        form = QuestionForm() #html페이지  폼 속성값  유지,저장?


    context= {'form':form}
    return render(request, 'pybo/question_form.html',context) # GET , #3번 form.is_valid(): else 인경우


#수정
@login_required(login_url='common:login')
def question_modify(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한없음')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)#기존instance값 보여주지만 리퀘값 덮어쓱시
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)


    else:
        form = QuestionForm(instance=question) #GET요청경우 질문수정화면에 조회된질문의 제목과내용이 반영될 수 있도록 폼생성

    context = {'form':form}
    return render(request,'pybo/question_form.html',context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request,'삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    question.delete()
    return redirect('pybo:index')
@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(type(request.user))
    print(type(request.user.username))
    print(type(question.author))
    print(request.user == question.author)
    if request.user == question.author:
        messages.error(request, '본인글은 추천 ㄴ')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)
