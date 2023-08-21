from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')      # User모델은 auth앱이 제공하는 모델이다.
    subject = models.CharField(max_length=200)      # 제목
    content = models.TextField()    # 내용
    create_date = models.DateTimeField()    # 생성일
    modify_date = models.DateTimeField(null=True, blank=True)   # null허용, .is_valid()로 검증 시 값이 없어도 됨.
    voter = models.ManyToManyField(User, related_name='voter_question')    # 추천인, user.voter_question.all()로 voter값을 얻을 수 있다

    def __str__(self):   # Question.objects.all()할 때, id값 대신 제목이 나타난다.
        return self.subject     # subject를 반환한다. 이게 없으면 id값이 반환됨

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)    # 질문(외래키), Question.answer_set으로 연결된 answer값을 가져올 수 있다.
    content = models.TextField()    # 내용
    create_date = models.DateTimeField()    # 생성일
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

# 모델을 변경한 후에는 반드시 python manage.py makemigrations, python manage.py migrate를 사용해야한다.



