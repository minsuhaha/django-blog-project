from django import forms
from .models import Post, Topic, Answer
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

# 답변 폼 추가생성 (9/17 폼 생성완료)
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }


