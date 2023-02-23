from django import forms
from pybo.models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']  # 진짜 연결시킬 항목을 작성
# 메타 데이터는 실제 데이터를 설명하는 데이터

        # widget = {
        #     'subject' : forms.TextInput(attrs={'class': 'form-control'}),
        #     'content' : forms.Textarea(attrs={'class': 'form-control', 'rows':10}),
        # }
