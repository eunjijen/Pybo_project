from django import forms
from pybo.models import Question, Answer, Comment

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']  # 진짜 연결시킬 항목을 작성

# 메타 데이터는 실제 데이터를 설명하는 데이터

        widgets = {
            'subject' : forms.TextInput(attrs={'placeholder': '제목을 입력하세요.'}),
            'content' : forms.Textarea(attrs={'placeholder': '내용을 입력하세요.'}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
