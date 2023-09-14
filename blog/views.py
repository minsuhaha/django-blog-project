import random
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views import View
from .forms import BlogForm
from .models import Post
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.files.storage import default_storage


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
def board_detail(request, post_id):
    post_detail = Post.objects.get(id = post_id)
    # 포스트 id로 게시물 가져옴
    if request.method == 'POST': 
        
        # 요청에 삭제가 포함된경우
        if 'delete-button' in request.POST:
            post_detail.delete()
            return redirect('board_detail.html')

    # 조회수 증가 및 db에 저장
    post_detail.views += 1 
    post_detail.save() 

    # 이전/다음 게시물 가져옴
    previous_post = Post.objects.filter(id__lt=post_detail.id, storage='Y').order_by('-id').first()
    next_post = Post.objects.filter(id__gt=post_detail.id, storage='Y').order_by('id').first()

    # 같은 주제인 게시물들 중 랜덤으로 가져옴
    recommended_posts = Post.objects.filter(topic=post_detail.topic, storage='Y').exclude(id=post_detail.id).order_by('?')

    # 랜덤으로 2개의 게시물 가져오기 (또는 원하는 개수로 조절)
    recommended_posts = random.sample(list(recommended_posts), 2)

    for recommended_post in recommended_posts:
        soup = BeautifulSoup(recommended_post.content, 'html.parser')
        image_tag = soup.find('img')
        recommended_post.image_tag = str(image_tag) if image_tag else ''
    
    context = {
        'post': post_detail,
        'previous_post': previous_post,
        'next_post': next_post,
        'recommended_posts': recommended_posts,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'board_detail.html', context)


# 이미지 업로드
class image_upload(View):
    
    # 사용자가 이미지 업로드 하는경우 실행
    def post(self, request):
        
        # file필드 사용해 요청에서 업로드한 파일 가져옴
        file = request.FILES['file']
        
        # 저장 경로 생성
        filepath = 'uploads/' + file.name
        
        # 파일 저장
        filename = default_storage.save(filepath, file)
        
        # 파일 URL 생성
        file_url = settings.MEDIA_URL + filename
        
        # 이미지 업로드 완료시 JSON 응답으로 이미지 파일의 url 반환
        return JsonResponse({'location': file_url})
