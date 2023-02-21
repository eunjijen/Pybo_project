from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.utils import timezone

# Create your views here.
def index(request):
    """
    pybo 목록 출력
    """
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}

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
    

