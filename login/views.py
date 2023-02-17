from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from member.models import Member
from member.forms import MemberCreationForm, LoginForm, ChangeProfileForm
from django.views.generic import View
import pdb
from PIL import Image
import os, io
from django.core.files.uploadedfile import InMemoryUploadedFile

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
    

def profile(request):
    user_id = None
    if request.user.is_authenticated:
        user_id = request.user.user_id  # 혹은 request.user.username 등 로그인한 유저의 정보를 사용

    if not user_id:
        return redirect('success')

    context = {
        'user_id': user_id,
        'name' : request.user.name,
        'int_stat' : request.user.int_stat,
        'social_stat' : request.user.social_stat,
        'exp_stat' : request.user.exp_stat,
        'total_exp' : request.user.total_exp,
        'title' : request.user.title,
        'title_color' : request.user.title_color,
        'profile_image' : request.user.profile_image,
    }


    return render(request, 'profile.html', {"context":context})

    
def change_profile(request):
    user_id = None
    if request.user.is_authenticated:
        user_id = request.user.user_id  # 혹은 request.user.username 등 로그인한 유저의 정보를 사용

    if not user_id:
        return redirect('success')

    if request.method == 'POST':
        form = ChangeProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile_image = form.cleaned_data['profile_image']
            member = Member.objects.get(user_id=user_id)
            img = Image.open(profile_image)
            img = img.convert('RGB')  # RGBA -> RGB 변환
            img = img.resize((100, 100))
            buffer = io.BytesIO()
            img.save(buffer, "JPEG")
            member.profile_image.save(profile_image.name, buffer, save=True)
            return redirect('profile')
    else:
        form = ChangeProfileForm()
    return render(request, 'change_profile.html', {'form': form })


