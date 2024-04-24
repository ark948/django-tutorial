import datetime
from django.test import TestCase
from django.utils import timezone

from polls.models import Question

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