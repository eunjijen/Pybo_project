from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..models import Question, Answer
from ..forms import AnswerForm


@login_required(login_url='common: login')
def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk = question_id)
    if request.method == 'POST':        # submit을 통한 POST 요청/처리
        form = AnswerForm(request.POST)  
        if form.is_valid():             # 유효성 검사
            answer = form.save(commit=False)    
            answer.author = request.user    # 로그인 사용자 정보로 설정
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()                # 인스턴스를 통해 db에 저장
            return redirect('pybo:detail', question_id = question.id)   

    else:    # GET 요청
        form = AnswerForm()      
    context = {'question': question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변 수정
    """
    answer = get_object_or_404(Answer, pk = answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id = answer.question.id)
    
    if request.method == "POST":
        form = AnswerForm(request.POST, instance = answer)
        if form.is_valid():
            answer = form.save(commit = False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id = answer.question.id)
    else:
        form = AnswerForm(instance = answer)

    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    pybo 답변 삭제
    """
    answer = get_object_or_404(Answer, pk = answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id = answer.question.id)