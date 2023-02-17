from .models import Member
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django import forms

class MemberCreationForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ['user_id', 'name', 'password1', 'password2']

    id_regex = RegexValidator(r'^[a-zA-Z0-9_-]+$', message='잘못된 형식의 ID입니다.')
    user_id = forms.CharField(
        #20자 이내의 영문, 숫자, 하이픈, 언더스코어만 허용
        max_length=20,
        required=True,
        validators=[id_regex],
    )

    def clean_id(self):
        user_id = self.cleaned_data['id']
        if not user_id:
            raise forms.ValidationError('ID를 입력해주세요.')
        return user_id    

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('비밀번호확인이 일치하지 않습니다.')
        return cleaned_data
    

class LoginForm(forms.Form):
    user_id = forms.CharField(label='아이디')
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
