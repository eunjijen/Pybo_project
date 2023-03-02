from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Question

def index(request):
    """
    pybo 목록 출력
    """
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw','')
    so = request.GET.get('so', 'recent')  # 정렬 기준

    # 조회
    # question_list = Question.objects.order_by('-create_date')

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter = Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer = Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')

    # 검색
    if kw:
        question_list = question_list.filter(
           Q(subject__icontains = kw) | # 제목검색
           Q(content__icontains = kw) | # 내용검색
           Q(author__username__icontains = kw) | # 질문 글쓴이 검색
           Q(answer__author__username__icontains = kw)  # 답글 글쓴이 검색
        ).distinct()
        # answer는 원래 answer_set

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩
    page_obj = paginator.get_page(page)
    
    # page와 kw를 추가
    context = {
        'question_list': page_obj,
        'kw': kw,
        'page': page,
        'so': so
        }
  
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)