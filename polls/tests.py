
import datetime

from django.test import TestCase
from django.utils import timezone
# url을 하드코딩하지 않도록 reverse를 import 한다.
from django.urls import reverse

from .models import Question


# Create your tests here.

class QuestionModelTests(TestCase):

    # 코드 작성시 함수 이름의 앞머리(prefix)도 test로 시작해야 한다.
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        # 현재시간에 30일을 더했다.
        time = timezone.now() + datetime.timedelta(days=30)
        # 미래시간의 질문을 생성한다.
        future_question = Question(pub_date=time)

        # 미래에 생성한 질문에 대한 생성일이 최근이냐 라고 호출햇을 때, 기대되어지는 결과 값은 False이다.
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


# test data를 만들기 위해 함수를 만듦. 함수를 호출하면 데이터 하나가 만들어 진다.
def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


# data는 각 테스트 함수마다 재설정되므로 필요할 때마다 그때그때 함수로 호출해서 만들어야 한다.
class QuestionIndexViewTests(TestCase):
    # data가 없는 경우
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        # data가 없는 경우 호출
        response = self.client.get(reverse('polls:index'))
        # 상태코드, 응답에 포함되어있는 내용, context가 비어있는지를 확인
        # 같은 값인지 비교하는 경우 Equal 사용
        self.assertEqual(response.status_code, 200)
        # 포함되어 있는지는 contain 사용
        self.assertContains(response, "No polls are available.")
        # queryset인 경우는 querysetEqual 사용
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    # data가 과거인 경우
    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        # data가 과거인 경우 호출
        create_question(question_text="Past question.", days=-30)
        # data 호출
        response = self.client.get(reverse('polls:index'))
        # data가 나오는지 확인, data가 나오지 않으면 문제가 있는 것
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    # data가 미래인 경우
    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        # data가 미래인 경우를 호출
        create_question(question_text="Future question.", days=30)
        # data 호출 => data가 나오면 문제가 있는 것
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    # 미래 data 하나, 과거 data 하나를 각각 만든 후 호출을 하면 과거 data만 나오는 것을 기대함.
    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    # 과거 data 두개를 만든 경우, 두개의 data가 기대되어진다.
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        # 질문을 만든다.
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        # test client가 호출한 후 결과를 받음
        response = self.client.get(url)
        # 결과를 통한 검증
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)