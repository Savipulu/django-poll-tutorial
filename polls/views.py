import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from django import forms

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class AddPollForm(forms.Form):
    question_text = forms.CharField(label="Question text", max_length=200)

    choice1 = forms.CharField(label="Choice 1", max_length=200)
    choice2 = forms.CharField(label="Choice 2", max_length=200)

    date_input = forms.DateInput()
    date_input.input_type = 'date'
    pub_date = forms.DateField(
        label="Publishing date", widget=date_input, initial=datetime.datetime.now())

    time_input = forms.TimeInput(format='%H:%M')
    time_input.input_type = 'time'
    pub_time = forms.TimeField(
        label="Publishing time", widget=time_input, initial=datetime.datetime.now())


class AddPollView(generic.FormView):
    template_name = 'polls/add.html'
    form_class = AddPollForm
    success_url = reverse_lazy('polls:index')

    def post(self, request):
        pub_date = datetime.date.fromisoformat(request.POST['pub_date'])
        pub_time = datetime.time.fromisoformat(request.POST['pub_time'])
        new_question = Question(
            question_text=request.POST['question_text'],
            pub_date=datetime.datetime.combine(pub_date, pub_time)
        )

        choice1 = Choice(question=new_question,
                         choice_text=request.POST['choice1'])
        choice2 = Choice(question=new_question,
                         choice_text=request.POST['choice2'])

        new_question.save()
        choice1.save()
        choice2.save()

        return HttpResponseRedirect(reverse('polls:index'))


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
