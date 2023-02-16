from .models import Member
from django.contrib.auth.forms import UserCreationForm
from django import forms

class MemberCreationForm(UserCreationForm):
    password_confirm = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ['id', 'name', 'password', 'password_confirm', 'profile_image']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('비밀번호확인이 일치하지 않습니다.')
        return cleaned_data
