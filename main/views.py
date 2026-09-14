from django.shortcuts import render
from main.models import Experience, Project

def show_main(request):
    context = {
        "name": "Delitha Theodora",
        "npm": "2506553585",
        "study_program": "Computer Science, International Class (2025-Present)",
        "bio": (
            "Hi, I'm Delitha Theodora! I'm a CS student at Universitas Indonesia focused on "
            "frontend engineering (Next.js) and UI/UX design (Figma). I build intuitive, responsive web "
            "applications as a stepping stone toward my ultimate goal: a career in cybersecurity."
        )
    }
    return render(request, "index.html", context)

def show_experience(request):
    context = {
        "name": "Delitha Theodora",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "components/experience.html", context)

def show_projects(request):
    context = {
        "name": "Delitha Theodora",
        "projects_list": Project.objects.all(),
    }
    return render(request, "components/projects.html", context)