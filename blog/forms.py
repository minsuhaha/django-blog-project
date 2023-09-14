from django import forms
from .models import Post, Topic
from ckeditor.widgets import CKEditorWidget  # CKEditor 위젯 추가


# 게시물 폼
class BlogForm(forms.ModelForm):

    # topic = forms.ModelChoiceField(
    #     queryset=Topic.objects.all(),
    #     label='토픽 선택',
    #     widget=forms.RadioSelect  # 라디오 선택 위젯 사용
    # )

    class Meta:
        model = Post
        fields = ['title', 'content', 'topic']



