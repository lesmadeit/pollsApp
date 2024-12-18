from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question




class IndexView(generic.ListView):
    template_name = 'pollster/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Return the last five published questions
        return Question.objects.order_by('-pub_date')[:5]



class DetailView(generic.DetailView):
    model = Question
    template_name = 'pollster/detail.html'



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'pollster/results.html'



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(render, 'pollster/detail.html',  {
            'question': question,
            'error_message': "You didn't selected a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # return an HttpResponseRedirect after successfully dealing To
        # prevent data from being posted twice if a user hits the Back button.
        return HttpResponseRedirect(reverse('pollster:results', args=(question.id,)))


