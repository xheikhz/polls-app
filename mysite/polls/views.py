from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Questions,Choice
from django.template import loader
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    template_name="polls/index.html"
    context_object_name="latest_questions_list"

    def get_queryset(self):
        return Questions.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date')[:5]

class DetailView(generic.DetailView):
    template_name='polls/detail.html'
    context_object_name='question'
    
    def get_queryset(self):
        return Questions.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date')[:5]
    

class ResultView(generic.DetailView):
    template_name='polls/result.html'
    context_object_name='question'

    def get_queryset(self):
        return Questions.objects.filter(pub_date__lte=timezone.now())
    




def vote(request,question_id):
    question=get_object_or_404(Questions,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{'question':question,'error_message':"you didn't select choice"})
    else:
        selected_choice.votes=F('votes')+1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result',args=(question.id,)))


