from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin  # For Validation  
from django.urls import reverse_lazy
from .models import Task

# Class based view for showing Task List
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'task'
# Sowing Only Particular User Data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = context['task'].filter(user=self.request.user)
        context['count'] = context['task'].filter(complete=False).count()
# Searching Task
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['task'] = context['task'].filter(title__icontains = search_input)
            context['search_input'] = search_input
        return context
# Class based View for sowing a particular task
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'app/task.html'

# Class based view for creating a new task
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    # fields = ['title', 'description']
    success_url = reverse_lazy('task')
# Used wwn we want to sow that while updating the task User Section don't come
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
# Class Based View for updating the task
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task')


#Class Based view for deleting the task
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task')

# Login Class based view, Use django based User model
class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('task')
    
# Class based View For Registration.

class RegisterPage(FormView):
    template_name = 'app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterPage, self).get(*args, *kwargs)