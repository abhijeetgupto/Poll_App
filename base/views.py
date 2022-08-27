from msilib.schema import ListView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Poll

# Class Based Views
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

# LOGIN AND REGISTER
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# # Celery
# import datetime
# from celery.schedules import crontab
# from celery.task import periodic_task
# from django.utils import timezone


# @periodic_task(run_every=crontab(minute='*/5'))
# def delete_old_orders():
#     d = timezone.now() - datetime.timedelta(hours=24)
#     # get expired orders
#     old = Poll.objects.filter(time_stamp=d)
#     # delete them
#     old.delete()


class CustomLoginView(LoginView):

    template_name = 'base/login.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('list-polls')


class RegisterUser(FormView):

    template_name = 'base/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login-page')

    def form_valid(self, form):
        form.save()
        return super(RegisterUser, self).form_valid(form)


class ListPoll(LoginRequiredMixin, ListView):

    template_name = 'base/list-polls.html'
    context_object_name = 'questions'
    model = Poll

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = Poll.objects.exclude(user=self.request.user)
        return context


class CreatePoll(LoginRequiredMixin, CreateView):
    template_name = 'base/create-poll.html'
    model = Poll
    fields = ['question', 'option1', 'option2', 'option3', 'option4']
    success_url = reverse_lazy('list-polls')

    def get_context_data(self, **kwargs):
        num_of_questions = len(Poll.objects.filter(user=self.request.user))
        flag = num_of_questions < 5
        context = super().get_context_data(**kwargs)
        context['can_create'] = flag
        context['num'] = num_of_questions
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatePoll, self).form_valid(form)


@login_required()
def PollDetail(request, pk):

    object = Poll.objects.get(pk=pk)
    if request.method == 'POST':
        option = request.POST.get('answer')
        print(type(option), option)

        if option == '1':
            object.vote1 += 1
            object.save()
            return redirect(PollResult, pk=pk)

        elif option == '2':
            object.vote2 += 1
            object.save()
            return redirect(PollResult, pk=pk)

        elif option == '3':
            object.vote3 += 1
            object.save()
            return redirect(PollResult, pk=pk)

        elif option == '4':
            object.vote4 += 1
            object.save()
            return redirect(PollResult, pk=pk)

    return render(request, 'base/poll-detail.html', {'object': object})


@login_required()
def PollResult(request, pk):
    object = Poll.objects.get(pk=pk)
    total_votes = object.vote1 + object.vote2 + object.vote3 + object.vote4
    op1 = op2 = op3 = op4 = 0
    if total_votes != 0:
        op1 = object.vote1*100/total_votes
        op2 = object.vote2*100/total_votes
        op3 = object.vote3*100/total_votes
        op4 = object.vote4*100/total_votes
    return render(request, 'base/poll-result.html', {'object': object, 'op1': op1, 'op2': op2, 'op3': op3, 'op4': op4})


@login_required
def UserProfile(request):

    user_questions = Poll.objects.filter(user=request.user)
    return render(request, 'base/profile.html', {'questions': user_questions})
