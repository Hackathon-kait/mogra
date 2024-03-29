from django.shortcuts import render,redirect
from .forms import SignupForm, LoginForm,EventsModelForm,ChangePasswordForm,ChangeUsernameForm,ChangeEmailForm,CustomPasswordResetForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from .models import EventsModel
from django.urls import reverse_lazy,reverse
from django.http.response import HttpResponse
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, 
    PasswordResetConfirmView, PasswordResetCompleteView
)
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
    template_name = 'mypage.html'
    
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

class DetailUpdateView(LoginRequiredMixin, UpdateView):
    model = EventsModel
    form_class = EventsModelForm
    success_url = '/home/'
    template_name = 'update.html'

class MyGraphView(LoginRequiredMixin,TemplateView):
    template_name = "graph.html"
    def get(self, request, *args, **kwargs):
        event_list = []
        eventnum = 0
        #ログイン中のユーザーのIDを取得
        user_id = self.request.user
        #ユーザーIDが一致する本を探す
        event = EventsModel.objects.filter(user=user_id).order_by('date_at')
        eventnum = EventsModel.objects.filter(user=user_id).order_by('date_at').count()
        event_list.extend(event)
        context = self.get_context_data(**kwargs)
        context["event_list"] = event_list
        context["eventnum"] = eventnum

        return self.render_to_response(context)
    
class ChangePasswordView(LoginRequiredMixin,View):
    template_name = 'passwordup.html'
    form_class = ChangePasswordForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.user.id)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user.id, data=request.POST)
        if form.is_valid():
            # 新しいパスワードをセットする
            user = request.user
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            # ユーザーを再認証してログインする
            user = authenticate(username=user.username, password=form.cleaned_data['new_password'])
            if user is not None:
                login(request, user)

            messages.success(request, 'パスワードを変更しました。')
            return redirect('/home/')
        return render(request, self.template_name, {'form': form})
    
class ChangeUsernameView(LoginRequiredMixin, View):
    form_class = ChangeUsernameForm
    template_name = 'usernameup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(user_id=request.user.id)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(user_id=request.user.id, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'アカウント名を変更しました。')
            return redirect('/home/')
        context = {'form': form}
        return render(request, self.template_name, context)
    
class ChangeEmailView(LoginRequiredMixin, View):
    form_class = ChangeEmailForm
    template_name = 'Emailup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class(user_id=request.user.id)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(user_id=request.user.id, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'メールアドレスを変更しました。')
            return redirect('/home/')
        return render(request, self.template_name, {'form': form})

class CustomPasswordResetView(PasswordResetView):
    form_class=CustomPasswordResetForm
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        """
        フォームがバリデーションを通過した場合に呼び出される
        """
        # 入力されたメールアドレスを取得
        email = form.cleaned_data['email']
        # メールアドレスが登録されているかチェック
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            # 登録されていない場合はエラーメッセージを表示
            form.add_error('email', 'このメールアドレスは登録されていません。')
            return self.form_invalid(form)
        # パスワードリセットのロジックを実装する
        return super().form_valid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
