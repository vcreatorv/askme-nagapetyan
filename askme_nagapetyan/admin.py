from django.contrib import admin
from .models import Question, Tag, Profile, Answer, QuestionLike, AnswerLike

# Register your models here.
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Answer)
admin.site.register(QuestionLike)
admin.site.register(AnswerLike)
