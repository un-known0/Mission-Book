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
        widget=forms.TextInput(attrs={'placeholder': '아이디'}),
    )
    name = forms.CharField(
        #20자 이내의 영문, 숫자, 하이픈, 언더스코어만 허용
        max_length=10,
        widget=forms.TextInput(attrs={'placeholder': '이름'}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 확인'}),
    )


    def clean_user_id(self):
        user_id = self.cleaned_data['user_id']
        if not user_id:
            self.cleaned_data['user_id'] = ''
            raise forms.ValidationError('ID를 입력해주세요.')
        try:
            Member.objects.get(user_id=user_id)
        except Member.DoesNotExist:
            return user_id
        self.cleaned_data['user_id'] = ''
        raise forms.ValidationError("이미 존재하는 ID입니다.")        

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('password2')
        # import pdb
        # pdb.set_trace()
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("두 비밀번호가 일치하지 않습니다.")
        return cleaned_data
        

class LoginForm(forms.Form):
    user_id = forms.CharField(
        label='아이디',
        widget=forms.TextInput(attrs={'placeholder': '아이디'})
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'})
    )


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['profile_image']


class ChangeNameForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name']
