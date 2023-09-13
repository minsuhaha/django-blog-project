from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import BlogForm
from .models import Post

# 게시글 작성
def board_write(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)  # request.FILES를 사용하여 이미지 처리
        print(form)
        if form.is_valid():
            # 폼 데이터를 모델에 저장
            form = form.save(commit=False)
            form.writer = request.user  # 현재 로그인한 사용자를 작성자로 설정
            form.save()
            return redirect('board')  # 성공 시 홈 페이지로 리디렉션
    else:
        form = BlogForm()
    return render(request, 'board_write.html', {'form': form})


# 사용자 로그인 뷰
def board_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('board')  # 로그인 성공 시 리디렉션할 페이지
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Create your views here.
def board(request):
    posts = Post.objects.all().order_by('-create_date')
    return render(request, 'board.html', {'posts': posts})

def board_detail(request):
    detail=Post.objects.all()
    return render(request,'board_detail.html',{'detail':detail})

