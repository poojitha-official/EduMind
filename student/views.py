from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Avg

from .models import (
    UserStudyProfile,
    TopicExplanation,
    InterviewQuestionSet,
    Quiz,
    QuizAttempt,
    ChatMessage,
)


def home(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not all([first_name, last_name, username, email, password, confirm_password]):
            messages.error(request, 'Please fill all fields.')
        elif len(password) < 6:
            messages.error(request, 'Password must have at least 6 characters.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            UserStudyProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('dashboard')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    profile, created = UserStudyProfile.objects.get_or_create(
        user=request.user
    )

    attempts = QuizAttempt.objects.filter(
        user=request.user,
        completed=True
    )

    average_score = attempts.aggregate(
        average=Avg('percentage')
    )['average'] or 0

    context = {
        'profile': profile,
        'topics_count': TopicExplanation.objects.filter(user=request.user).count(),
        'interviews_count': InterviewQuestionSet.objects.filter(user=request.user).count(),
        'quizzes_count': Quiz.objects.filter(user=request.user).count(),
        'completed_quizzes': attempts.count(),
        'average_score': round(average_score, 2),
        'recent_topics': TopicExplanation.objects.filter(user=request.user).order_by('-created_at')[:5],
        'recent_quizzes': attempts.order_by('-created_at')[:5],
        'recent_interviews': InterviewQuestionSet.objects.filter(user=request.user).order_by('-created_at')[:5],
    }

    return render(request, 'dashboard.html', context)


@login_required
def topic_explainer(request):
    topics = TopicExplanation.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'topic_explainer.html', {'topics': topics})


@login_required
def chat(request):
    chat_messages = ChatMessage.objects.filter(
        user=request.user
    ).order_by('created_at')

    return render(request, 'chat.html', {'chat_messages': chat_messages})


@login_required
def interview_prep(request):
    interview_sets = InterviewQuestionSet.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'interview_prep.html', {
        'interview_sets': interview_sets
    })


@login_required
def quiz_generator(request):
    quizzes = Quiz.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'quiz_generator.html', {'quizzes': quizzes})


@login_required
def history(request):
    context = {
        'topics': TopicExplanation.objects.filter(user=request.user).order_by('-created_at'),
        'interviews': InterviewQuestionSet.objects.filter(user=request.user).order_by('-created_at'),
        'quizzes': Quiz.objects.filter(user=request.user).order_by('-created_at'),
    }

    return render(request, 'history.html', context)