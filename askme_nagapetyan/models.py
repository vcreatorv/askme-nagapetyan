from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count


# Create your models here.

class QuestionManager(models.Manager):
    def hot(self):
        return self.annotate(likes_count=Count('question_like')).order_by('-likes_count')

    def new(self):
        return self.order_by('-created_at')


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', related_name='questions')

    class Meta:
        db_table = 'question'

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.user.username


class Answer(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'answer'

    def __str__(self):
        return f"Answer to {self.question.title} by {self.author.username}"


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')
        db_table = 'question_like'


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'answer')
        db_table = 'answer_like'
