from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count


# Create your models here.

class QuestionManager(models.Manager):
    def with_related(self):
        return self.select_related('author').prefetch_related('tags')

    def hot(self):
        return self.with_related().annotate(likes_count=Count('likes')).order_by('-likes_count')

    def new(self):
        return self.with_related().order_by('-created_at')


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def answer_count(self):
        return self.answers.count()

    def like_count(self):
        return self.likes.count()

    class Meta:
        db_table = 'question'


class TagManager(models.Manager):
    def popular(self):
        return self.annotate(question_count=Count('questions')).order_by('-question_count')[:10]


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    objects = TagManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tag'


class ProfileManager(models.Manager):
    def get_top_users(self):
        return self.select_related('user').annotate(answer_count=Count('user__answers')).order_by('-answer_count')[:5]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'profile'


class Answer(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer to {self.question.title} by {self.author.username}"

    def like_count(self):
        return self.likes.count()

    class Meta:
        db_table = 'answer'


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')
        db_table = 'question_like'


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'answer')
        db_table = 'answer_like'
