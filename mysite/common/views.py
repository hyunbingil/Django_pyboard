from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        # 입력으로 전달받은 데이터를 이용해 사용자 생성(POST 요청)
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # 입력값을 개별적으로 얻고 싶은 경우에 사용하는 함수
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            # 신규 사용자를 저장한 후에 자동 로그인
            login(request, user)
            return redirect('index')
    else:
        # common/signup.html 템플릿을 호출 (GET 요청)
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})