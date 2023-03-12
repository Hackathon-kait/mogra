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
