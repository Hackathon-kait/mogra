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
 
class MyLogoutView(LoginRequiredMixin,LogoutView):
    template_name = 'logout.html'

class MyUserView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class EventDetailView(DetailView):
    model = EventsModel
    template_name = 'detail.html'
    context_object_name = 'event'
    pk_url_kwarg = 'uuid'
    
class MyEventCreateView(CreateView):
    template_name = 'create.html'
    form_class = EventsModelForm
    success_url = '/home/'
    
    def form_valid(self, form):
        new_event=form.save(commit=False)
        new_event.user=self.request.user
        new_event.save()
        
        result = super().form_valid(form)
        return result
    
class DetailDeleteView(LoginRequiredMixin,DeleteView):
    template_name = "detail.html"
    model = EventsModel
    success_url = '/home/'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
#詳細情報を更新
class DetailUpdateView(LoginRequiredMixin, UpdateView):
    model = EventsModel
    form_class = EventsModelForm
    success_url = '/home/'
    template_name = 'update.html'