from django.core.management.base import BaseCommand
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta
from django.core.cache import cache
from app.models import Question, Answer, Profile



class Command(BaseCommand):
    help = 'Обновляет кэш топ пользователей'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Начало обновления кэша топ пользователей"))
        cache_key = "top_users"
        one_week_ago = now() - timedelta(days=7)

        questions = Question.objects.filter(created_at__gte=one_week_ago)
        answers = Answer.objects.filter(created_at__gte=one_week_ago)

        total_scores = {}

        for question in questions:
            user_id = question.author.id  
            total_scores[user_id] = total_scores.get(user_id, 0) + question.like_count() 

        for answer in answers:
            user_id = answer.author.id
            total_scores[user_id] = total_scores.get(user_id, 0) + answer.like_count()

        top_users = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)[:10]

        top_profiles = Profile.objects.filter(user__in=[user_id for user_id, _ in top_users])

        cache.set(cache_key, top_profiles, 60)
        self.stdout.write(self.style.SUCCESS("Топ пользователей успешно обновлен"))
