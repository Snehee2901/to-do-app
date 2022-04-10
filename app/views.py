from dataclasses import field, fields
import imp
from multiprocessing import context
from re import search, template
from sre_constants import SUCCESS
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task

# Create your views here.
#tasks --> tasklist

class registeruser(FormView):
    template_name='app/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(registeruser,self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasklist')
        return super(registeruser, self).get(*args, **kwargs)

class customLogin(LoginView):
    template_name = 'app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasklist')


class Tasklist(LoginRequiredMixin , ListView):
    model = Task
    context_object_name='tasklist'

    # getting user specific data
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["tasklist"] = context['tasklist'].filter(user=self.request.user) #getting user
        context["count"] = context['tasklist'].filter(complete=False).count() #getting count of incomplete items

        search_inp = self.request.GET.get("searcharea") or ''

        if search_inp:
            context['tasklist'] = context['tasklist'].filter(title__contains = search_inp)
        
        context['searchinp'] = search_inp
        return context
        

class Taskdetail(LoginRequiredMixin ,DetailView):
    model = Task
    context_object_name = 'task'

class CreateTask(LoginRequiredMixin ,CreateView):
    model = Task
    # import all the fields
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasklist')

    #setting user value to logged in user to add task

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask,self).form_valid(form)

class Taskupdate(LoginRequiredMixin ,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasklist')

class Taskdelete(LoginRequiredMixin,DeleteView):
    model = Task
    fields ='__all__'
    success_url = reverse_lazy('tasklist')