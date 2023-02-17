from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from member.models import Member
from member.forms import MemberCreationForm, LoginForm
from django.views.generic import View
import pdb

def join(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('success')
    else:
        form = MemberCreationForm()
    return render(request, 'join.html', {'form': form })

def success(request):#테스트용
    user_id = None
    if request.user.is_authenticated:
        user_id = request.user.user_id  # 혹은 request.user.username 등 로그인한 유저의 정보를 사용

    context = {
        'user_id': user_id
    }
    return render(request, 'success.html', {"context":context})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            user = authenticate(request, user_id=user_id, password=password)
            # pdb.set_trace()
            if user is not None:
                login(request, user)
                return redirect('success')
            else:
                form.add_error('user_id', '아이디 또는 비밀번호가 일치하지 않습니다.')
        return render(request, 'login.html', {'form': form})