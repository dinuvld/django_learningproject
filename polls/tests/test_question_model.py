import datetime

from django.utils import timezone
from django.test import TestCase

from polls.models import Question


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently should return False if its pub_date is
        in the future.
        """

        time = timezone.now() + datetime.timedelta(days = 5)
        future_question = Question(pub_date = time)
        self.assertEqual(future_question.was_published_recently(), False)


    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently should return False if its pub_date is
        not within the last day.
        """
        time = timezone.now() - datetime.timedelta(days = 5)
        old_question = Question(pub_date = time)
        self.assertEqual(old_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently should return True if its pub_date is
        within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours = 2)
        recent_question = Question(pub_date = time)
        self.assertEqual(recent_question.was_published_recently(), True)
