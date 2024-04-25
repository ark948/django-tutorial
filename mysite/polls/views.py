from typing import Any
from django.db.models import F
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Question, Choice

class IndexView(generic.ListView):
    # by default, looks for <model_name>_list.html
    template_name = "polls/index.html"
    # overriding the default context name which is question_list
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions (not including those set in future)."""
        # lte -> less than or eqaul to
        # return questions whose pub_date is less than or eqaul to right now.
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    

class DetailView(generic.DetailView):
    # context variable is automatically provided because of the model
    model = Question
    # by default, DetailView will look for <model_name>_detail.html template
    template_name = "polls/detail.html"

    def get_queryset(self):
        """Exclude any questions that aren't published yet."""
        # return only questions that are less or equal than current time
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))