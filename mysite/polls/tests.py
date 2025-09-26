from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Questions
from django.urls import reverse

class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        time=timezone.now()+datetime.timedelta(days=30)
        future_question=Questions(pub_date=time)
        self.assertIs(future_question.was_publishedrecently(),False)
    
    def test_was_published_recently_with_old_question(self):
        time=timezone.now()-datetime.timedelta(days=1,seconds=1)
        old_question=Questions(pub_date=time)
        self.assertIs(old_question.was_publishedrecently(),False)

    def test_was_published_recently_with_recent_questions(self):
        time=timezone.now()-datetime.timedelta(hours=23,minutes=59,seconds=59)
        recent_question=Questions(pub_date=time)
        self.assertIs(recent_question.was_publishedrecently(),True)

def create_question(question_text,days):
    time=timezone.now+datetime.timedelta(days=days)
    return Questions.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'no polls are available')
        self.assertQuerySetEqual(response.context['latest_questions_list'],[])

    def test_past_questions(self):
        question=create_question(question_text='past question',days=-30)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_questions_list'],[question],)

    def test_future_questions(self):
        create_question(question_text='future questions',days=30)
        response=self.client.get(reverse('polls:index'))
        self.assertContains(response,'no polls are available')
        self.assertQuerySetEqual(response.context['latest_questions_list'],[])

    def test_future_questions_and_past_questions(self):
        question=create_question(question_text='past questions',days=-30)
        create_question(question_text='future questions',days=30)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_questions_list'],[question])

    def test_two_past_questions(self):
        question1=create_question(question_text='question 1',days=-30)
        question2=create_question(question_text='question 2',days=-5)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_questions_list'],[question1,question2])

class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        future_question=create_question(question_text='future question',days=5)
        url=reverse('polls:detail',args=(future_question.id,))
        response=self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_past_question(self):
        past_question=create_question(question_text='past question',days=-5)
        url=reverse('polls:detail',args=(past_question.id,))
        response=self.client.get(url)
        self.assertContains(response,past_question.question_text)