from django.urls import path
from rest_framework.authtoken import views as authtoken_views

from main import api_views

app_name = "api"

urlpatterns = [
    path("auth/token/", authtoken_views.obtain_auth_token, name="token-auth"),
    path("auth/logout/", api_views.api_logout, name="logout"),
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", api_views.project_star, name="project-star"),
    path("blog/", api_views.blog_list, name="blog-list"),
    path("blog/<uuid:blog_id>/", api_views.blog_detail, name="blog-detail"),
    path("blog/<uuid:blog_id>/star/", api_views.blog_star, name="blog-star"),
]
