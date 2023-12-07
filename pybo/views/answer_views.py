from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.http import HttpResponseNotAllowed

from ..forms import AnswerForm
from ..models import Question, Answer


@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST": # 요청 입력 시
        form = AnswerForm(request.POST) # 임시 내용을 저장할 Form 객체 생성
        if form.is_valid(): # Form의 내용이 존재한다면
            answer = form.save(commit=False)    # 컨텐츠 내용 임시저장
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now() # 현재 시간 저장
            answer.question = question          # 외래키 내용 저장
            answer.save()                       # 실제 데이터베이스 저장
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id)) # 리다이렉트로 동일한 페이지에 다른 화면이 출력되도록 한다.
    else:
        return HttpResponseNotAllowed('Only POST is possible.') # Get 방식을 허용하지 않아 무조건 내용을 입력하게 한다.
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context) # 질문의 답변을 표시하기 위한 코드

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))