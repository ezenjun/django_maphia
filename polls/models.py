
import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class Question(models.Model):  # 하나의 question에 여려개의 Choice를 갖는 구조

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        # 미래에 생성된 데이터는 최근으로 간주하지 않는다. 미래의 날짜는 거짓으로 나와야한다.
        now = timezone.now()
        # question 생성 날짜가 미래로 넘어가지 않도록, 현재날짜를 두고 최근 기준을 하루로 두었다.
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # customizing한 field에 대해서 속성을 부여하여 편리성을 향상시킬 수 있다.
    # admin_order_field는 field typaclassy정렬을 위한 기준을 명시해준다.
    # 기준을 발행일로 하겠다는 이야기이다.
    was_published_recently.admin_order_field = 'pub_date'
    # boolean은 bool을 주면 true false 라는 문자 모습에서 아이콘 모습으로 보여준다.
    was_published_recently.boolean = True
    # description은 타이트를 변경시켜주는 속성이다.
    was_published_recently.short_description = 'Published recently?'

    # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    # 최근 데이터냐 아니냐를 반환하는 함수
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

