from django.shortcuts import render, redirect
from main.forms import ProjectForm, BlogForm, ExperienceForm
from main.models import Experience, Project, BlogPost
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDeniad

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'No active login session / Cookie not found')
    context = {
        "name": "Delitha Theodora",
        "npm": "2506553585",
        "study_program": "Computer Science, International Class (2025-Present)",
        "bio": (
            "Hi, I'm Delitha Theodora! I'm a CS student at Universitas Indonesia focused on "
            "frontend engineering (Next.js) and UI/UX design (Figma). I build intuitive, responsive web "
            "applications as a stepping stone toward my ultimate goal: a career in cybersecurity."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)

def show_experience(request):
    """
    Renders the Experience section of the portfolio.
    Fetches experience data by internally calling the JSON API endpoint
    and deserializing the response into Django model instances.
    """
    json_response = get_experience_json(request)

    experience_list = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience_list = [exp.object for exp in experience_list]

    context = {
        "name": "Delitha Theodora",
        "experience_list": experience_list,
    }
    return render(request, "components/experience.html", context)

@login_required(login_url="/login/")
def create_experience(request):
    """
    Handles the creation of a new Experience entry.
    Processes POST data through the ExperienceForm and redirects 
    on success, or renders the empty/invalid form on GET/failure.
    """
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience has been added!")
        return redirect("main:show_experience")

    context = {
        "form": form,
    }
    return render(request, "forms/experience_form.html", context)

@login_required(login_url="/login/") 
def update_experience(request, exp_id):
    """
    Handles updating an existing Experience entry by its UUID.
    Pre-fills the ExperienceForm with the instance's current data.
    """
    experience = get_object_or_404(Experience, pk=exp_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience has been updated!")
        return redirect("main:show_experience")

    context = {
        "form": form,
        "is_update": True,
    }
    return render(request, "forms/experience_form.html", context)

def get_experience_json(request):
    """
    API endpoint that returns all Experience records in JSON format,
    ordered by their creation date (newest first).
    """
    experiences = Experience.objects.all().order_by('-started_at')
    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

@login_required(login_url="/login/") 
def delete_experience(request, exp_id):
    """
    Handles the deletion of a specific Experience entry by its UUID.
    Requires a POST request (typically via a confirmation modal form) 
    to execute the deletion.
    """
    experience = get_object_or_404(Experience, pk=exp_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience has been deleted.")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Delitha",
        "projects_list": projects,
        "title_query": title_query,
    }
    return render(request, "components/projects.html", context)

# def show_projects(request):
#     context = {
#         "name": "Delitha Theodora",
#         "projects_list": Project.objects.all(),
#     }
#     return render(request, "components/projects.html", context)

def show_blog(request):
    json_response = get_blogs_json(request)

    blog_list = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    blog_list = [blog.object for blog in blog_list]

    context = {
        'blog_list': blog_list,
    }
    return render(request, "components/blog.html", context)

@login_required(login_url="/login/")
def create_blog(request):
    form = BlogForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New blog post has been added!")
        return redirect("main:show_blog")

    context = {
        "form": form,
    }
    return render(request, "forms/blog_form.html", context)

def update_blog(request, blog_id):
    blog = get_object_or_404(BlogPost, pk=blog_id)
    form = BlogForm(request.POST or None, instance=blog)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Blog post has been updated!")
        return redirect("main:show_blog")

    context = {
        "form": form,
        "is_update": True,
    }
    return render(request, "forms/blog_form.html", context)

def get_blogs_json(request):
    blogs = BlogPost.objects.all().order_by('-date_posted')
    blogs_json = serializers.serialize("json", blogs)
    return HttpResponse(blogs_json, content_type="application/json")

@login_required(login_url="/login/") 
def delete_blog(request, blog_id):
    blog = get_object_or_404(BlogPost, pk=blog_id)

    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog post has been deleted.")
        return redirect("main:show_blog")

    return redirect("main:show_blog")

@login_required(login_url="/login/")
def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New project has been added!")
        return redirect("main:show_projects")

    context = {
        "name": "Delitha",
        "form": form,
    }
    return render(request, "forms/projects_form.html", context)

def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project has been updated!")
        return redirect("main:show_projects")

    context = {
        "name": "Delitha",
        "form": form,
        "is_update": True,
    }
    return render(request, "forms/projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

@login_required(login_url="/login/") 
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project has been deleted.")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("main:login")

    context = {
        "name": "Delitha",
        "form": form,
    }
    return render(request, "components/register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Delitha",
        "form": form,
    }
    return render(request, "components/login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response