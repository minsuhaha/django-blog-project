from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import BlogForm
from .models import Post


# 게시물 작성 - board write page
def board_write(request):
    if request.user.is_authenticated:
        # 사용자가 로그인한 경우에만 실행
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


# 게시물 수정 - board write page
@login_required(login_url='board_login')
def board_modify(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.writer:
        messages.error(request, '수정권한이 없습니다')
        return redirect('board_detail', post_id=post.id)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('board_detail', post_id=post.id)
    else:
        form = BlogForm(instance=post)
    context = {'form': form}
    return render(request, 'board_write.html', context)

# 게시물 삭제 - board detail page
@login_required(login_url='board_login')
def board_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.writer:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('board_detail', post_id=post.id)
    post.delete()
    return redirect('board')


# 로그인 - login page
def board_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('board')  # 로그인 성공 시 리디렉션할 페이지
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# 로그아웃 - logout page
def board_logout(request):
    logout(request)
    return redirect('board')



# 메인 게시판 - board page
def board(request, topic=None):

    if topic:
        posts = Post.objects.filter(topic=topic, publish='Y').order_by('-views')
    else:
        posts = Post.objects.filter(publish='Y').order_by('-views') 
    
    title_post = Post.objects.all().order_by('-view').first()
    return render(request, 'board.html', {'posts': posts ,'title_post':title_post})



# 상세 페이지 - board detail page
def board_detail(request,id):
    post_detail = Post.objects.filter('id' == id)
    return render(request, 'board_detail.html')
