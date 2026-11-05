
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserStudyProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="study_profile"
    )
    current_streak = models.IntegerField(default=0)
    last_study_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class TopicExplanation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="topic_explanations"
    )
    topic = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=30)
    summary = models.TextField(blank=True)
    analogy = models.TextField(blank=True)
    explanation = models.TextField(blank=True)
    code_example = models.TextField(blank=True)
    takeaways = models.TextField(blank=True)
    interview_tips = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic


class InterviewQuestionSet(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="interview_sets"
    )
    subject = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=30)
    number_of_questions = models.IntegerField(default=5)
    questions = models.TextField(default="[]", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject + " - " + self.role


class Quiz(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="quizzes"
    )
    topic = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=30)
    number_of_questions = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="questions"
    )
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=1)
    explanation = models.TextField(blank=True)

    def __str__(self):
        return self.question_text[:100]


class QuizAttempt(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="quiz_attempts"
    )
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="attempts"
    )
    answers = models.TextField(default="{}", blank=True)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    percentage = models.FloatField(default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " - " + self.quiz.topic


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_messages"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " - " + self.role


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        UserStudyProfile.objects.get_or_create(user=instance)
