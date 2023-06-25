from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer


##아래 생성뷰
   # answer 모델 직접참조
    # answer = Answer(question=question,content=request.POST.get('content'),
    #                create_date=timezone.now())
    # answer.save()
@login_required(login_url='common:login') #로그인이필요한 함수 ,함수가실행되면 자동으로 로그인화면이동
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)

    else:
        form = AnswerForm()

    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)




@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request,'수정권한없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date=timezone.now()
            answer.save()

            print('user', answer.author)
            print('answer.id', answer.id)
            print('answer.question.id', answer.question.id)
            print('answer.question', answer.question)
            print('answer.question.subject', answer.question.subject)
            return redirect('pybo:detail', question_id=answer.question.id)

    else:
        form = AnswerForm(instance=answer)

    context = {'answer':answer,'form': form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭 제 권 한 이 없 습 니 다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)


@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user == answer.author:
        messages.error(request, '본인글은 추천 ㄴ')
    else:
        answer.voter.add(request.user)
    return redirect('pybo:detail', question_id=answer.question.id)