from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import EventsModel
from django.forms.widgets import DateInput

class SignupForm(UserCreationForm):
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
            'eevaluation': '評価',
            'date_at': '日時',
        }
        widgets = {
                'date_at': DateInput(attrs={'type': 'date'})
        }
    def clean_evaluation(self):
        value = self.cleaned_data['evaluation']
        if value >= 11:
            raise forms.ValidationError('10以下の値を入力してください。')
        return value