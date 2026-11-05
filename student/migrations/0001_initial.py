
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserStudyProfile",
            fields=[
                ("id", models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name="ID"
                )),
                ("current_streak", models.IntegerField(default=0)),
                ("last_study_date", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="study_profile",
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),
        migrations.CreateModel(
            name="TopicExplanation",
            fields=[
                ("id", models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name="ID"
                )),
                ("topic", models.CharField(max_length=200)),
                ("subject", models.CharField(max_length=100)),
                ("difficulty", models.CharField(max_length=30)),
                ("summary", models.TextField(blank=True)),
                ("analogy", models.TextField(blank=True)),
                ("explanation", models.TextField(blank=True)),
                ("code_example", models.TextField(blank=True)),
                ("takeaways", models.TextField(blank=True)),
                ("interview_tips", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="topic_explanations",
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),
        migrations.CreateModel(
            name="InterviewQuestionSet",
            fields=[
                ("id", models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name="ID"
                )),
                ("subject", models.CharField(max_length=100)),
                ("role", models.CharField(max_length=100)),
                ("difficulty", models.CharField(max_length=30)),
                ("number_of_questions", models.IntegerField(default=5)),
                ("questions", models.TextField(blank=True, default="[]")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="interview_sets",
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),
        migrations.CreateModel(
            name="Quiz",
            fields=[
                ("id", models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name="ID"
                )),
                ("topic", models.CharField(max_length=200)),
                ("subject", models.CharField(max_length=100)),
                ("difficulty", models.CharField(max_length=30)),
                ("number_of_questions", models.IntegerField(default=5)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="quizzes",
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),
        migrations.CreateModel(
            name="ChatMessage",
            fields=[
                ("id", models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name="ID"
                )),
                ("role", models.CharField(
                    choices=[("user", "User"), ("assistant", "Assistant")],
                    max_length=10
                )),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="chat_messages",
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),
        migrations.CreateModel(
            name="QuizQuestion",
            fields=[
                ("id", models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name="ID"
                )),
                ("question_text", models.TextField()),
                ("option_a", models.CharField(max_length=500)),
                ("option_b", models.CharField(max_length=500)),
                ("option_c", models.CharField(max_length=500)),
                ("option_d", models.CharField(max_length=500)),
                ("correct_answer", models.CharField(max_length=1)),
                ("explanation", models.TextField(blank=True)),
                ("quiz", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="questions",
                    to="student.quiz"
                )),
            ],
        ),
        migrations.CreateModel(
            name="QuizAttempt",
            fields=[
                ("id", models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name="ID"
                )),
                ("answers", models.TextField(blank=True, default="{}")),
                ("score", models.IntegerField(default=0)),
                ("total_questions", models.IntegerField(default=0)),
                ("percentage", models.FloatField(default=0)),
                ("completed", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("quiz", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="attempts",
                    to="student.quiz"
                )),
                ("user", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="quiz_attempts",
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),
    ]
