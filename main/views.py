from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from main.forms import ProjectForm, BlogForm, ExperienceForm
from main.models import Experience, Project, BlogPost
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

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
    title_query = request.GET.get("title", "").strip()

    context = {
        "title_query": title_query,
        "form": ExperienceForm(),
    }
    return render(request, "components/experience.html", context)

@login_required(login_url="/login/")
def create_experience(request):
    """
    Handles the creation of a new Experience entry.
    Processes POST data through the ExperienceForm and redirects 
    on success, or renders the empty/invalid form on GET/failure.
    """
    if not request.user.has_perm('main.add_experience'):
        raise PermissionDenied
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
    if not request.user.has_perm('main.change_experience'):
        raise PermissionDenied
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
    API endpoint that returns a JSON representation of Experience records.
    Supports optional filtering by title using the 'title' GET parameter.
    Results are ordered by descending 'started_at' date.

    Returns:
        JsonResponse: A list of dictionaries containing the serialized 
        fields and primary keys for each experience entry.
    """
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all().order_by('-started_at')
    
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for exp in experiences:
        data.append({
            "pk": str(exp.id),
            "fields": {
                "title": exp.title,
                "description": exp.description,
                "category_display": exp.get_category_display(),
                "thumbnail": exp.thumbnail,
                "is_ongoing": exp.is_ongoing,
            }
        })
    return JsonResponse(data, safe=False)

@login_required(login_url="/login/") 
def delete_experience(request, exp_id):
    """
    Handles the deletion of a specific Experience entry by its UUID.
    Requires a POST request (typically via a confirmation modal form) 
    to execute the deletion.
    """
    if not request.user.has_perm('main.delete_experience'):
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=exp_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience has been deleted.")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Delitha",
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "components/projects.html", context)

# def show_projects(request):
#     context = {
#         "name": "Delitha Theodora",
#         "projects_list": Project.objects.all(),
#     }
#     return render(request, "components/projects.html", context)

def show_blog(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "title_query": title_query,
        "form": BlogForm(),
    }
    return render(request, "components/blog.html", context)

@login_required(login_url="/login/")
def create_blog(request):
    if not request.user.has_perm('main.add_blogpost'):
        raise PermissionDenied
    form = BlogForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New blog post has been added!")
        return redirect("main:show_blog")

    context = {
        "form": form,
    }
    return render(request, "forms/blog_form.html", context)

@login_required(login_url="/login/")
def update_blog(request, blog_id):
    if not request.user.has_perm('main.change_blogpost'):
        raise PermissionDenied
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
    """
    API endpoint that returns a JSON representation of BlogPost records.
    Supports optional filtering by title using the 'title' GET parameter.
    Prefetches the 'starred_by' field to optimize database queries, 
    preventing N+1 query problems when calculating star counts.

    Returns:
        JsonResponse: A list of serialized blog objects, including 
        metadata such as total stars and whether the current logged-in 
        user has starred the post.
    """
    title_query = request.GET.get("title", "").strip()
    blogs = BlogPost.objects.prefetch_related('starred_by').all().order_by('-date_posted')
    
    if title_query:
        blogs = blogs.filter(title__icontains=title_query)

    data = []
    for blog in blogs:
        starred_users = blog.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(blog.id),
            "fields": {
                "title": blog.title,
                "content": blog.content,
                "snippet": blog.snippet,
                "date_posted": blog.date_posted.strftime('%b. %d, %Y'),
                "read_time": blog.read_time,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/") 
def delete_blog(request, blog_id):
    if not request.user.has_perm('main.delete_blogpost'):
        raise PermissionDenied
    blog = get_object_or_404(BlogPost, pk=blog_id)

    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog post has been deleted.")
        return redirect("main:show_blog")

    return redirect("main:show_blog")

@login_required(login_url="/login/")
def create_project(request):
    if not request.user.has_perm('main.add_project'):
        raise PermissionDenied
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

@login_required(login_url="/login/")
def update_project(request, project_id):
    if not request.user.has_perm('main.change_project'):
        raise PermissionDenied
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
    """
    API endpoint that returns a JSON representation of all Project records.
    Supports filtering by title using the 'title' GET parameter.
    Uses 'prefetch_related' on 'starred_by' to efficiently bulk-load 
    many-to-many relationship data for star calculations.

    Returns:
        JsonResponse: A list of project objects with their core fields, 
        plus calculated 'star_count' and 'is_starred' metadata.
    """
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "demo_link": project.demo_link,
                "image": project.image,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/") 
def delete_project(request, project_id):
    if not request.user.has_perm('main.delete_project'):
        raise PermissionDenied
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

@login_required(login_url="/login/")
def toggle_star_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)
    return redirect("main:show_projects")

@login_required(login_url="/login/")
def toggle_star_blog(request, blog_id):
    blog = get_object_or_404(BlogPost, pk=blog_id)
    if request.method == "POST":
        if request.user in blog.starred_by.all():
            blog.starred_by.remove(request.user)
        else:
            blog.starred_by.add(request.user)
    return redirect("main:show_blog")

@require_POST
def create_project_ajax(request):
    """
    Asynchronously creates a new Project entry via an AJAX POST request.
    
    Security:
        - Requires POST method via @require_POST.
        - Verifies that the user has the 'main.add_project' permission.
    
    Processing:
        - Validates the incoming POST data using ProjectForm.
        - On success, saves the record and returns HTTP 201 Created.
        - On failure, returns HTTP 400 Bad Request with a JSON map of errors.

    Returns:
        JsonResponse: Contains a success message and primary key, or error details.
    """
    if not request.user.has_perm('main.add_project'):
        return JsonResponse(
            {"message": "Only the portfolio owner can add projects."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Project added successfully.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@require_POST
def create_blog_ajax(request):
    """
    Asynchronously creates a new BlogPost entry via an AJAX POST request.
    
    Security:
        - Strict check for POST method and 'main.add_blogpost' permission.
    
    Returns:
        JsonResponse (201): If form is valid, returns the new post's PK.
        JsonResponse (400): If form is invalid, returns validation errors.
        JsonResponse (403): If the user lacks permission.
    """
    if not request.user.has_perm('main.add_blogpost'):
        return JsonResponse(
            {"message": "Only the portfolio owner can add blog posts."},
            status=403,
        )

    form = BlogForm(request.POST)
    if form.is_valid():
        blog = form.save()
        return JsonResponse(
            {"message": "Blog post added successfully.", "pk": str(blog.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@require_POST
def create_experience_ajax(request):
    """
    Asynchronously creates a new Experience entry via an AJAX POST request.
    
    Security:
        - Enforces POST method using @require_POST.
        - Validates user role via 'main.add_experience' permission.
    
    Returns:
        JsonResponse: A status 201 with the created object's ID, or 
        status 400/403 with descriptive error messages.
    """
    if not request.user.has_perm('main.add_experience'):
        return JsonResponse(
            {"message": "Only the portfolio owner can add experience."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience added successfully.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)