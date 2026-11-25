from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import BlogPost, Project
from main.permissions import (
    IsPortfolioOwnerOrEditorOrReadOnly, IsPortfolioOwnerOrReadOnly,
)
from main.serializers import BlogPostSerializer, ProjectSerializer

# Authentication for every view below comes from DEFAULT_AUTHENTICATION_CLASSES
# in settings.py: token auth for the mobile app, session auth for the website.


@api_view(["GET", "HEAD", "POST"])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    if request.method in ("GET", "HEAD"):
        projects = Project.objects.prefetch_related("starred_by").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            projects = projects.filter(title__icontains=title)
        serializer = ProjectSerializer(projects, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = ProjectSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related("starred_by"), pk=project_id,
    )

    if request.method in ("GET", "HEAD"):
        serializer = ProjectSerializer(project, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProjectSerializer(
        project, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    # Always star as request.user; the client can't choose another account
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    serializer = ProjectSerializer(project, context={"request": request})
    return Response(serializer.data)


def blog_queryset():
    return BlogPost.objects.prefetch_related("starred_by").order_by("-date_posted", "title")


@api_view(["GET", "HEAD", "POST"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def blog_list(request):
    if request.method in ("GET", "HEAD"):
        blogs = blog_queryset()
        title = request.query_params.get("title", "").strip()
        if title:
            blogs = blogs.filter(title__icontains=title)
        serializer = BlogPostSerializer(blogs, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = BlogPostSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def blog_detail(request, blog_id):
    blog = get_object_or_404(blog_queryset(), pk=blog_id)

    if request.method in ("GET", "HEAD"):
        serializer = BlogPostSerializer(blog, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = BlogPostSerializer(
        blog, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def blog_star(request, blog_id):
    blog = get_object_or_404(BlogPost, pk=blog_id)
    # Always star as request.user; the client can't choose another account
    if blog.starred_by.filter(pk=request.user.pk).exists():
        blog.starred_by.remove(request.user)
    else:
        blog.starred_by.add(request.user)
    # Reload so the star fields reflect the change
    blog = blog_queryset().get(pk=blog.pk)
    serializer = BlogPostSerializer(blog, context={"request": request})
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_logout(request):
    # request.auth is the Token row when the caller used token auth, and None
    # when they used the website session. Deleting the row revokes the token,
    # so later requests with it get 401.
    if isinstance(request.auth, Token):
        request.auth.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
