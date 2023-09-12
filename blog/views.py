from django.shortcuts import render
from .models import Post

# Create your views here.
def board(request):
    posts = Post.objects.all().order_by('-create_date')
    return render(request, 'board.html', {'posts': posts})
