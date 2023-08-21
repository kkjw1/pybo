from django import forms
from pybo.models import Question, Answer
# form은 페이지 요청시 전달되는 피라미터들을 쉽게 관리하기 위해 사용하는 클래스.
class QuestionForm(forms.ModelForm):    # 모델과 연결된 폼으로 폼을 저장하면 연결된 모델의 데이터를 저장할 수 있다.
    class Meta:
        model = Question    # 사용할 모델
        fields = ['subject', 'content'] # QuestionForm에서 사용할 Question 모델의 속성
        labels = {
            'subject': '제목',    # 라벨값을 줘서 영문을 한국어로 나타냄
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답 변 내 용',
        }


