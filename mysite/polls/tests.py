import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question

def create_question(question_text, days):
    # if days is a positive integer, post will be published in future
    # if negative, in past
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns a 404 not found."""
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no question exist, an appropriate message is displayed."""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the index page."""
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """Questions with pub_date in future, are not dispalyed in the index page."""
        question = create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed."""
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"], [question],)
        
    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"], [question2, question1],)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """Returns False for questions whose pub_date is in future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        # this is ought to be false, should be false
        # if was_published_recently return true, test will fail
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Retruns False for questions whose pub_date is older than 1 day. (not recent)"""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        # create an question object with at least 24 hours and one second age
        old_quesiton = Question(pub_date=time)
        self.assertIs(old_quesiton.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)