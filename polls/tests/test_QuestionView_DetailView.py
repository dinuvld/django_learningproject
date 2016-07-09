from django.core.urlresolvers import reverse
from polls.models import Question
from django.utils import timezone
from django.test import TestCase


def create_question(question_Text, days):
    """
    Creates a question with the text question_Text and an offset
    of days (negative for qeustionss already published, positive for questions
    that have yet to be published, 0 questions published right now.
    """
    time = timezone.now() + timezone.timedelta(days = days)
    return Question.objects.create(question_Text = question_Text,
                                   pub_date = time)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropiate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available for the moment.")
        self.assertQuerysetEqual(response.context['latestQuestionList'], [])

    def test_index_view_with_past_question(self):
        """
        If questions exist they should appear
        """
        create_question(question_Text = "Past question", days = -5)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Past question")
        self.assertQuerysetEqual(response.context['latestQuestionList'],
                                 ['<Question: Past question>'])

    def test_index_view_with_future_question(self):
        """
        Questions with a pub_date in the future should not be
        displayed on the index page.
        """
        create_question(question_Text = "Future question", days = 5)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available for the moment.")
        self.assertQuerysetEqual(response.context['latestQuestionList'], [])

    def test_index_view_with_past_and_future_question(self):
        """
        If both past and future questions exist only the ones from the
        past should be displayed on the index page
        """
        create_question(question_Text = "Future question", days = 5)
        create_question(question_Text = "Past question", days = -5)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Past question")
        self.assertQuerysetEqual(response.context['latestQuestionList'],
                                 ["<Question: Past question>"])

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_Text="Past question 1.", days=-30)
        create_question(question_Text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latestQuestionList'],
            ['<Question: Past question 2.>',
             '<Question: Past question 1.>'])


class DetailViewTests(TestCase):
    def test_detail_view_with_past_question(self):
        """
        The detail view should display the question's text
        """
        past_question = create_question(question_Text = "Past question",
                                        days = -5)
        url = reverse('polls:detail', args = (past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_Text)

    def test_detail_view_with_future_question(self):
        """
        The DetailView should raise a 404 error when someone tries
        to acces via URL a question that is not yet published.
        """
        future_question = create_question(question_Text = "Future question",
                                          days = 5)
        url = reverse('polls:detail', args = (future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
