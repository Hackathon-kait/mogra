from django.shortcuts import render
from .forms import SignupForm, LoginForm,EventsModelForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from .models import EventsModel
from django.urls import reverse_lazy
from django.http.response import HttpResponse
# Create your views here.

class MograView(TemplateView):
    template_name='index.html'


class MySignupView(CreateView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = '/home/'
    
    def form_valid(self, form):
        result = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return result

class MyLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm

class GraphView():
   template_name = 'graph.html'
 
class MyLogoutView(LogoutView):
    template_name = 'logout.html'

class MyUserView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class MyOtherView(LoginRequiredMixin, TemplateView):
    template_name = 'login_app/other.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(username=self.request.user.username)
        return context
 """