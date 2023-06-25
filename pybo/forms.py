from django import forms
from pybo.models import Question ,Answer


###https://docs.djangoproject.com/en/4.0/topics/forms/ 장고 폼 설명
class QuestionForm(forms.ModelForm):
    class Meta:
         model = Question  # 사용할 모델
         fields = ['subject','content']  ## QuestionForm 에서 사용할 Question 모델의 속성
         labels = {
           'subject': '제목',
           'content': '내용',
         }

        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}), # 부트스트랩 적용
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        # }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
                'content': '답 변 내 용',
                 }