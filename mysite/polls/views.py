from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from polls.models import Question, Choice

# first argument is HttpRequest
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list
    }
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    # tries to aquire a question object from the database, given an id from the url
    question = get_object_or_404(Question, pk=question_id)
    # if question object was found,
    # each question has a number of choices
    # the following, will try to aquire that choice from post data
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        # request is dict, returns id element of submitted data
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
    # if the choice, was found, the user can vote on it
    else:
        # F("votes") -> instructs the database to increase the vote count by 1
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # After somebody votes a choice in a question, it will be redirected to results page
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))