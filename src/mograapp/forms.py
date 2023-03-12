from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import EventsModel
from django.forms.widgets import DateInput
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class SignupForm(UserCreationForm):
    username = forms.CharField(label="氏名",max_length=254, required=True, help_text='')
    email = forms.EmailField(label="メールアドレス",max_length=254, required=True, help_text='')
    password1 = forms.CharField(label="パスワード",max_length=254, required=True,widget=forms.PasswordInput,help_text='')
    password2 = forms.CharField(label="パスワード再入力",max_length=254, required=True,widget=forms.PasswordInput,help_text='')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスはすでに登録されています。")
        return email
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class LoginForm(AuthenticationForm):
    pass

class EventsModelForm(forms.ModelForm):
    class Meta:
        model = EventsModel
        fields = ['title', 'detail', 'evaluation','date_at']
        
        labels = {
            'title': 'タイトル',
            'detail': '詳細',
            'evaluation': '評価',
            'date_at': '日時',
        }
        widgets = {
                'date_at': DateInput(attrs={'type': 'date'}),
        }
    def clean_evaluation(self):
        value = self.cleaned_data['evaluation']
        if value >= 11:
            raise forms.ValidationError('10以下の値を入力してください。')
        return value

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label="現在のパスワード", widget=forms.PasswordInput())
    new_password = forms.CharField(label="新しいパスワード", widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(label="新しいパスワード再入力", widget=forms.PasswordInput())

    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        user = User.objects.get(id=self.user_id)
        if not user.check_password(current_password):
            raise ValidationError('現在のパスワードが間違っています。')
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')
        if new_password and confirm_new_password and new_password != confirm_new_password:
            self.add_error('confirm_new_password', 'パスワードが一致しません。')
        return cleaned_data


class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField(label="新しいアカウント名")
    password = forms.CharField(label="現在のパスワード", widget=forms.PasswordInput())

    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data['password']
        user = User.objects.get(id=self.user_id)
        if not authenticate(username=user.username, password=password):
            raise ValidationError('パスワードが間違っています。')
        return password

    def clean_new_username(self):
        new_username = self.cleaned_data['new_username']
        if User.objects.filter(username=new_username).exists():
            raise ValidationError('このアカウント名は既に使われています。')
        return new_username

    def save(self):
        user = User.objects.get(id=self.user_id)
        user.username = self.cleaned_data['new_username']
        user.save()
        

class ChangeEmailForm(forms.Form):
    current_email = forms.EmailField(label='現在のメールアドレス')
    new_email = forms.EmailField(label='新しいメールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
        super().__init__(*args, **kwargs)

    def clean_current_email(self):
        current_email = self.cleaned_data['current_email']
        user = User.objects.get(id=self.user_id)
        if current_email != user.email:
            raise ValidationError('現在のメールアドレスが正しくありません。')
        return current_email

    def clean_new_email(self):
        new_email = self.cleaned_data['new_email']
        if User.objects.filter(email=new_email).exists():
            raise ValidationError('このメールアドレスは既に使われています。')
        return new_email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        user = authenticate(username=User.objects.get(id=self.user_id).username, password=password)
        if not user:
            raise ValidationError('パスワードが正しくありません。')
        return cleaned_data

    def save(self):
        user = User.objects.get(id=self.user_id)
        user.email = self.cleaned_data['new_email']
        user.save()

