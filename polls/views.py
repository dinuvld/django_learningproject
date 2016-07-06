from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from polls.models import Question, Choice


def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.doesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',
                                    args = (question_id,)))


def detail(request, question_id):
    try:
        question = Question.objects.get(pk = question_id)
    except Question.doesNotExist:
        raise Http404("Question does not exits! :( ")
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def index(request):
    latestQuestionList = Question.objects.order_by("-pub_date")[:5]
    context = {
        'latestQuestionList': latestQuestionList,
    }
    return render(request, 'polls/index.html', context)
