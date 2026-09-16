from django.shortcuts import render
from main.forms import ProjectForm
from main.models import Experience, Project, BlogPost
from django.core.paginator import Paginator
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

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

def show_blog(request):
    blog_list = BlogPost.objects.all().order_by('-date_posted')

    paginator = Paginator(blog_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'blog_list': page_obj,
        'page_obj': page_obj
    }
    return render(request, "components/blog.html", context)

def create_object(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New project has been added!")
        return redirect("main:show_projects")

    context = {
        "name": "Delitha",
        "form": form,
    }
    return render(request, "projects_form.html", context)