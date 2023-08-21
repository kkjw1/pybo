from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from ..models import Question # base_views.py는 더 하위에 존재하므로 ..models로 모듈을 import한다.

# 장고 페이징, 데이터를 묶는 것
def index(request):
    page = request.GET.get('page', '1')         # get방식으로 호출된 url에서 page값을 가져옴
    kw = request.GET.get('kw', '')      # 검색어
    question_list = Question.objects.order_by('-create_date')   # 생성날짜 역순으로 정렬된 qestion 리스트
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색, 제목에 kw 문자열이 포함되는지를 의미한다
            Q(content__icontains=kw) |  # 내용 검색, __를 이용하여 하위 속성에 접근할 수 있다.
            Q(answer__content__icontains=kw) |   # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10)    # 페이지당 10개씩
    page_obj = paginator.get_page(page)         # page에 해당하는 페이징 객체를 생성, 장고 내부적으로는 해당 페이지의 데이터만 조회 함.
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    # question = Question.objects.get(id=question_id)   # pybo/40 을 요청하면 오류코드 500(서버오류)이 나타남
    question = get_object_or_404(Question, pk=question_id)  # 없는 데이터를 요청 시에 오류코드 404(페이지를 찾을 수 없을 때)가 나타나게 해준다.
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
