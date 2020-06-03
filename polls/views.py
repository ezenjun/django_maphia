from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


# client에게서 request를 받으면, request에는 여러 정보가 담겨 있다.  그리고 다시 Response 해준다!
# Response하기 전 데이터 저장, 추출 등의 과정을 할 것임..
# 요청된 페이지의 내용이 담긴 HttpResponse 객체를 반환하거나, 혹은 Http404 같은 예외를 발생하게 해야합니다.

# context에서 사용할 이름이 model 이름과 다르다면, context_object_name을 다시 정해준다.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    # 필요한 함수를 get_queryset함수를 통해서 다시 작성해주면 된다.
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        # 큰 값은 duty 사용, contaim 등 많은 키워드 존재
        return Question.objects.filter(
            # __lte는 less than equal로, 현재시간보다 작거나 같은 data를 가져오도록 한다.
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

        # """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]


# render함수를 사용하게 되면, 코드 양을 줄일 수 있다.
# Shorcuts이라고해서 정형화된 작업은 소스코드를 줄이기 위해 간단한 함수로 제공된다.
# render를 사용하게되면 loader, HttpResponse를 import하지 않고 render로 명시 후 한줄로 작성하면 된다.
# def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    context = {
#        'latest_question_list': latest_question_list,
#    }
#    return render(request, 'polls/index.html', context)

# 사용할 template 이름, 해당 template에서 사용할 데이터의 모델을 넘겨준다.
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


# try except 처리 없이 shortcuts만으로 처리 => 동일하게 작동
# def detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/detail.html', {'question': question})

# question에 data가 없는 경우, question id를 전달 받고
# question을 조회했을 때 data가 없으면 Question does not exist하고 보여진다.
# try:
#    question = Question.objects.get(pk=question_id)
# except Question.DoesNotExist:
#    raise Http404("Question does not exist")
# return render(request, 'polls/detail.html', {'question': question})

# return HttpResponse("You're looking at question %s." % question_id)

# 선택지에 대한 vote를 1추가하고, 결과페이지를 보여주게 된다.
# 해당 url이 보여지게 되고 resert url에서 result view를 호출할 것이다.

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# def results(request, question_id):
# question조회 후 result template이 결과페이지로 넘어간다.
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/results.html', {'question': question})

# response = "You're looking at the results of question %s."
# return HttpResponse(response % question_id)

# view를 호출 할 때 question_id를 넘겨 받음.
# post방식으로 데이터 조회하는 경우.. (get방식으로도 가능. 코드 지정해줘야함. if, elif로)
# post는 데이터 생성, 수정 / get은 조회를 위해 호출
def vote(request, question_id):
    # if request.method == 'GET' :
    #    do_something()
    # question id를 조회
    # elif request.method == 'POST':
    question = get_object_or_404(Question, pk=question_id)
    try:
        # 이 question에 대해 외래키를 받는 선택지를 가져오게 된다.
        # 조건: 선택지 중에서 pk값이 template에서 넘겨받은 값을 조회하게 된다.
        # request는 template에서 POST방식으로 호출
        # 'choice'는 name칸의 입력 값이다. name의 data를 가지고 와라!
        # name의 data가 없을 경우, except로 예외발생..
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # 상세페이지(polls/detai.html)로 response
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            # context msg로는 question과 error msg를 보내주게 된다.
            'question': question,
            'error_message': "You didn't select a choice.",
            # error msg는 detail template에서 있다. error msg 데이터가 없으면 "You ~~ choice."를 보여준다.
        })  # context변수를 별도로 선언하지 않고 데이터를 보낼 수도 있음.
    else:  # 데이터가 있는 경우는 선택지에 대해 표를 1 더한 후 저장한다. (Result url로 redirect해준다.)
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # responseredirect는 post와 한 세트로 생각.
        # url을 하드코딩하지 않기위해 reverse를 사용해서 appname, urlname을 사용했다.
    # return HttpResponse("You're voting on question %s." % question_id)

# question data중에서 출판일자를 5개까지만 정렬하여 데이터를 가져옴.
# 이 데이터를 ','로 연결하여 string으로 만들겠다
# 그 문자열을 Response하겠다.
# def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    output = ', '.join([q.question_text for q in latest_question_list])
#    return HttpResponse(output)

# client에게서 request를 받으면, request에는 여러 정보가 담겨 있다.  그리고 다시 Response 해준다!
# Response하기 전 데이터 저장, 추출 등의 과정을 할 것임..
# 요청된 페이지의 내용이 담긴 HttpResponse 객체를 반환하거나, 혹은 Http404 같은 예외를 발생하게 해야합니다.

# context를 통해서 template의 데이터를 전달해준다. latest_question_list의 데이터를 template에 전달한다.
# def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('polls/index.html')
#    context = {
#        'latest_question_list': latest_question_list,
#    }
#    return HttpResponse(template.render(context, request))