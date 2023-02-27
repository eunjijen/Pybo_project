from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page','1')  # 페이지
    # 조회
    question_list = Question.objects.order_by('-create_date')
    # 페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}

    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common: login')
def question_create(request):
    """
    pybo 질문등록
    """
    if request.method == 'POST':        # submit을 통한 POST 요청/처리
        form = QuestionForm(request.POST)  
        
        if form.is_valid():             # 유효성 검사
            question = form.save(commit=False)    # db에는 반영하지 마라
            question.author = request.user
            question.create_date = timezone.now()
            question.save()                # 인스턴스를 통해 db에 저장
            return redirect('pybo:index')   # get으로 바꾸기 위해 redirect 목록보기로 이동

    else:    # GET 요청
        form = QuestionForm()      # 클래스 생성  내용이 비어있는 form이 템플릿으로 넘어가

    context = {'form':form}      # 유효성 검사 결과 false라면 여기로 옴
    return render(request, 'pybo/question_form.html', context)
# db에 저장을 못하면 랜더링으로 넘어가


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문 수정
    """
    question = get_object_or_404(Question, pk = question_id)
    if request.user != question.author:  # 권한 없음 403 에러
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id = question.id)
    
    if request.method == "POST":
        # 질문 수정을 위해 값 덮어쓰기
        form = QuestionForm(request.POST, instance = question)
        if form.is_valid():
            question = form.save(commit = False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id = question.id)
    else:
        # 질문 수정 화면에 기존 제목, 내용 반영
        form = QuestionForm(instance = question)
        context = {'form': form}
        return render(request, 'pybo/question_form.html', context)
# 405 에러는 메소드 잘못

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk = question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', qusetion_id = question.id)
    question.delete()
    return redirect('pybo:index')
    


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

