from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Count
from django.conf import settings
from .models import Feedback


def index(request):
    """College Home Page"""
    return render(request, "feedback/index.html")


def home(request):
    """Student Feedback Form"""

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        degree = request.POST.get("degree")
        year = request.POST.get("year")
        course = request.POST.get("course")

        q1 = request.POST.get("q1")
        q2 = request.POST.get("q2")
        q3 = request.POST.get("q3")
        q4 = request.POST.get("q4")
        q5 = request.POST.get("q5")
        q6 = request.POST.get("q6")
        q7 = request.POST.get("q7")
        q8 = request.POST.get("q8")
        q9 = request.POST.get("q9")
        q10 = request.POST.get("q10")

        overall_rating = q10
        comment = request.POST.get("comment")

        if not all([
            name, email, degree, year, course,
            q1, q2, q3, q4, q5,
            q6, q7, q8, q9, q10,
            comment
        ]):
            messages.error(request, "Please fill all fields.")
            return render(request, "feedback/home.html")

        feedback = Feedback(
            name=name,
            email=email,
            degree=degree,
            year=year,
            course=course,
            q1=q1,
            q2=q2,
            q3=q3,
            q4=q4,
            q5=q5,
            q6=q6,
            q7=q7,
            q8=q8,
            q9=q9,
            q10=q10,
            overall_rating=overall_rating,
            comment=comment
        )

        feedback.save()

        try:
            send_mail(
                "Feedback Submitted Successfully",
                f"Dear {name},\n\nThank you for submitting your feedback.",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print("MAIL ERROR:", e)

        messages.success(request, "Thank you for your feedback!")
        return redirect("home")

    return render(request, "feedback/home.html")


def admin_login(request):
    """Admin Login"""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, "Login Successful.")
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid Username or Password.")

    return render(request, "feedback/admin_login.html")


@login_required
def admin_dashboard(request):
    """Admin Dashboard"""

    feedbacks = Feedback.objects.all().order_by("-timestamp")

    degree = request.GET.get("degree")
    year = request.GET.get("year")
    course = request.GET.get("course")
    rating = request.GET.get("rating")

    if degree:
        feedbacks = feedbacks.filter(degree=degree)

    if year:
        feedbacks = feedbacks.filter(year=year)

    if course:
        feedbacks = feedbacks.filter(course=course)

    if rating:
        feedbacks = feedbacks.filter(overall_rating=rating)

    courses = Feedback.objects.values("course").annotate(
        count=Count("course")
    ).order_by("course")

    context = {
        "feedbacks": feedbacks,
        "courses": courses,

        "current_degree": degree,
        "current_year": year,
        "current_course": course,
        "current_rating": rating,

        "total_feedback": feedbacks.count(),
        "excellent_count": feedbacks.filter(overall_rating="Excellent").count(),
        "good_count": feedbacks.filter(overall_rating="Good").count(),
        "average_count": feedbacks.filter(overall_rating="Average").count(),
        "poor_count": feedbacks.filter(overall_rating="Poor").count(),
    }

    return render(request, "feedback/admin_dashboard.html", context)

@login_required
def mark_addressed(request, feedback_id):
    feedback = Feedback.objects.get(id=feedback_id)
    feedback.status = "addressed"
    feedback.save()

    messages.success(request, "Feedback marked as Addressed.")
    return redirect("admin_dashboard")


@login_required
def delete_feedback(request, feedback_id):
    feedback = Feedback.objects.get(id=feedback_id)
    feedback.delete()

    messages.success(request, "Feedback deleted successfully.")
    return redirect("admin_dashboard")


def admin_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("admin_login")