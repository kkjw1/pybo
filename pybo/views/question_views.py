from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

# 질문 등록
@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)   # request.POST에 담긴 subject, content 값이 QuestionForm 의 subject, content 속성에 자동으로 저장되어 객체가 생성
        if form.is_valid(): # form이 유효하다면, 작성된 값이 올바르지 않으면 실패
            question = form.save(commit=False)  # 임시 저장하여 question 객체를 리턴받는다.
            question.author = request.user
            question.create_date = timezone.now()   # 작성일시 설정, Question속성에 create_date가 있기 떄문에
            question.save() # 데이터를 실제로 저장
            return redirect('pybo:index')
    else:
        form = QuestionForm() #  로그아웃 상태에서 “답변등록” 버튼을 누르더라도 로그인 수행후 405 오류가 발생하지 않고 상세화면으로 돌아감
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


# 질문 수정
@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author: # 수정하려는 질문의 글쓴이가 다른 경우
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question) # instance 를 기준으로 QuestionForm 을 생성하지만 request.POST의 값으로 덮어씌움
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question) # GET요청인 경우 조회된 질문의 제목과 내용이 반영될 수 있도록 폼을 생성함.
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

# 질문 삭제
@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

# 질문 추천
@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        question.voter.add(request.user)    # add()함수를 사용하여 추가
    return redirect('pybo:detail', question_id=question.id)

