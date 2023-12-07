# from django.shortcuts import render, get_object_or_404, redirect
# from django.utils import timezone
# from django.http import HttpResponseNotAllowed
# from .models import Question, Answer
# from .forms import QuestionForm, AnswerForm
# from django.core.paginator import Paginator # paging
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages


# def index(request):
#     page = request.GET.get('page','1') # 페이지 디폴트 값인 '1' 값 호출
#     question_list = Question.objects.order_by('-create_date')
#     paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
#     page_obj = paginator.get_page(page) # 데이터 일부(전체가 아닌)만 조회하는 쿼리를 선언하는 객체 생성
#     context = {'question_list': page_obj} # question_list는 페이징 객체(page_obj)
#     # context = {'question_list': question_list}
#     return render(request, 'pybo/question_list.html', context)

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk = question_id)
#     context = {'question': question}
#     return render(request, 'pybo/question_detail.html', context)

# @login_required(login_url='common:login')
# def answer_create(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     if request.method == "POST": # 요청 입력 시
#         form = AnswerForm(request.POST) # 임시 내용을 저장할 Form 객체 생성
#         if form.is_valid(): # Form의 내용이 존재한다면
#             answer = form.save(commit=False)    # 컨텐츠 내용 임시저장
#             answer.author = request.user  # author 속성에 로그인 계정 저장
#             answer.create_date = timezone.now() # 현재 시간 저장
#             answer.question = question          # 외래키 내용 저장
#             answer.save()                       # 실제 데이터베이스 저장
#             return redirect('pybo:detail', question_id=question.id) # 리다이렉트로 동일한 페이지에 다른 화면이 출력되도록 한다.
#     else:
#         return HttpResponseNotAllowed('Only POST is possible.') # Get 방식을 허용하지 않아 무조건 내용을 입력하게 한다.
#     context = {'question': question, 'form': form}
#     return render(request, 'pybo/question_detail.html', context) # 질문의 답변을 표시하기 위한 코드

# @login_required(login_url='common:login')
# def answer_modify(request, answer_id):
#     answer = get_object_or_404(Answer, pk=answer_id)
#     if request.user != answer.author:
#         messages.error(request, '수정권한이 없습니다')
#         return redirect('pybo:detail', question_id=answer.question.id)
#     if request.method == "POST":
#         form = AnswerForm(request.POST, instance=answer)
#         if form.is_valid():
#             answer = form.save(commit=False)
#             answer.modify_date = timezone.now()
#             answer.save()
#             return redirect('pybo:detail', question_id=answer.question.id)
#     else:
#         form = AnswerForm(instance=answer)
#     context = {'answer': answer, 'form': form}
#     return render(request, 'pybo/answer_form.html', context)

# @login_required(login_url='common:login')
# def answer_delete(request, answer_id):
#     answer = get_object_or_404(Answer, pk=answer_id)
#     if request.user != answer.author:
#         messages.error(request, '삭제권한이 없습니다')
#     else:
#         answer.delete()
#     return redirect('pybo:detail', question_id=answer.question.id)

# @login_required(login_url='common:login')
# def question_create(request):
#     if request.method == 'POST':
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             question = form.save(commit=False)
#             question.author = request.user  # author 속성에 로그인 계정 저장
#             question.create_date = timezone.now()
#             question.save()
#             return redirect('pybo:index')
#     else:
#         form = QuestionForm()
#     context = {'form': form}
#     return render(request, 'pybo/question_form.html', context)

# @login_required(login_url='common:login')
# def question_modify(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     if request.user != question.author:
#         messages.error(request, '수정권한이 없습니다')
#         return redirect('pybo:detail', question_id=question.id)
#     if request.method == "POST":
#         form = QuestionForm(request.POST, instance=question)
#         if form.is_valid():
#             question = form.save(commit=False)
#             question.modify_date = timezone.now()  # 수정일시 저장
#             question.save()
#             return redirect('pybo:detail', question_id=question.id)
#     else:
#         form = QuestionForm(instance=question)
#     context = {'form': form}
#     return render(request, 'pybo/question_form.html', context)

# @login_required(login_url='common:login')
# def question_delete(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     if request.user != question.author:
#         messages.error(request, '삭제권한이 없습니다')
#         return redirect('pybo:detail', question_id=question.id)
#     question.delete()
#     return redirect('pybo:index')
