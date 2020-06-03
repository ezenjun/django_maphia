from django.urls import path

from . import views

#client가 false라고 호출하게 되면 views.index라는 view를 호출하게 된다.
# 해당 주소로 index view가 호출된다.

#만약 5를 전달한다면 상세페이지에 대한 view를 호출하게 된다.
# polls/views.py의 detail값을 response(클라이언트에게 전달)하게 된다.

# path(패턴/호출할 값/url패턴 명시 대신 작성할 템플릿..?)
# question_id는 view에 있는 매개변수 중 qusetion_id와 일치되어야 한다.

#경로문자열에서 일치하는 패턴들의 이름이 <question_id>에서 <pk>로 변경되었다.
# 일반적인 것이라 django에 구현이 이미 되어있음.
# pk는 db내의 하나의 열 즉, 하나의 데이터를 구분할 수 있는 값이다. pk값은 중복되지 않는다.
app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

#urlpatterns = [
    # ex: /polls/
#   path('', views.index, name='index'),
    # ex: /polls/5/
#    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
#    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
#    path('<int:question_id>/vote/', views.vote, name='vote'),
#]

