from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.utils import timezone
from .forms import QuestionForm
from django.core.paginator import Paginator

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

def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    # print(request.method)
    # print(request.GET)     # dict
    # print(request.POST)    # dict

    # content = request.POST['content']     # 1. 키가 없으면 예외 발생
    # print('[content]', content)

    # content = request.POST.get('content') # 2. 키가 없으면 None 리턴
    # print('get(content)', content)


    question = get_object_or_404(Question, pk = question_id)
    question.answer_set.create(content = request.POST.get('content'),
                               create_date = timezone.now())
    
    return redirect('pybo:detail', question_id = question.id)
    

def question_create(request):
    """
    pybo 질문등록
    """
    if request.method == 'POST':        # submit을 통한 POST 요청/처리
        form = QuestionForm(request.POST)  
        if form.is_valid():             # 유효성 검사
            question = form.save(commit=False)    # db에는 반영하지 마라
            question.create_date = timezone.now()
            question.save()                # 인스턴스를 통해 db에 저장
            return redirect('pybo:index')   # get으로 바꾸기 위해 redirect 목록보기로 이동

    else:    # GET 요청
        form = QuestionForm()      # 클래스 생성  내용이 비어있는 form이 템플릿으로 넘어가

    context = {'form':form}      # 유효성 검사 결과 false라면 여기로 옴
    return render(request, 'pybo/question_form.html', context)
# db에 저장을 못하면 랜더링으로 넘어가