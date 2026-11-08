import uuid

from django.contrib.auth.models import Group, Permission, User
from django.urls import NoReverseMatch, reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import BlogPost, Project


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": "Python",
            "demo_link": "https://example.com/", "image": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": " "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"demo_link": "javascript:alert(1)"}, "demo_link"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")

        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_blank_image_uses_default(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.data["image"], "img/blank-folder.svg")

    def test_owner_gets_404_for_missing_project(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        response = self.client.patch(url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_head_is_public(self):
        self.assertEqual(self.client.head(self.list_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.head(self.detail_url).status_code, status.HTTP_200_OK)

    def test_star_only_accepts_post(self):
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class EditorHTMLProjectTest(APITestCase):
    """The API is superuser-only, but Editor keeps the HTML project views from Assignment 4."""

    def setUp(self):
        editor_group = Group.objects.create(name="Editor")
        editor_group.permissions.set(Permission.objects.filter(
            codename__in=["add_project", "change_project", "delete_project"],
        ))
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(editor_group)
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.client.login(username="editor", password="test-password")

    def test_editor_can_use_html_project_pages(self):
        self.assertEqual(self.client.get(reverse("main:create_project")).status_code, 200)
        update_url = reverse("main:update_project", args=[self.project.id])
        self.assertEqual(self.client.get(update_url).status_code, 200)

        response = self.client.post(update_url, {
            "title": "Edited", "description": "My website", "tech_stack": "Django",
            "demo_link": "", "image": "img/blank-folder.svg",
        })
        self.assertRedirects(response, reverse("main:show_projects"))
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Edited")

        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.exists())

    def test_editor_cannot_write_through_api(self):
        url = reverse("api:project-detail", args=[self.project.id])
        self.assertEqual(self.client.patch(url, {"title": "Changed"}, format="json").status_code, 403)

    def test_old_project_routes_still_resolve(self):
        for name in ["show_projects", "get_projects_json", "create_project", "create_project_ajax"]:
            self.assertTrue(reverse(f"main:{name}"))
        for name in ["update_project", "delete_project", "toggle_star_project"]:
            self.assertTrue(reverse(f"main:{name}", args=[self.project.id]))


class BlogPostAPITest(APITestCase):
    """Assignment 6: the four roles on /api/v1/blog/."""

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.regular = User.objects.create_user(username="regular", password="test-password")
        # Like the real Editor group, which also has add/delete perms:
        # the API must still only allow PUT/PATCH for Editor.
        editor_group = Group.objects.create(name="Editor")
        editor_group.permissions.set(Permission.objects.filter(
            codename__in=["add_blogpost", "change_blogpost", "delete_blogpost", "view_blogpost"],
        ))
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(editor_group)

        self.blog = BlogPost.objects.create(
            title="Hackathon recap", content="What I learned.", read_time=3,
        )
        self.list_url = reverse("api:blog-list")
        self.detail_url = reverse("api:blog-detail", args=[self.blog.id])
        self.star_url = reverse("api:blog-star", args=[self.blog.id])
        self.payload = {"title": "New post", "content": "Fresh content", "read_time": 5}

    def assertBlogUnchanged(self):
        self.assertEqual(BlogPost.objects.count(), 1)
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.title, "Hackathon recap")
        self.assertEqual(self.blog.content, "What I learned.")

    # Reading

    def test_everyone_can_read_list_and_detail(self):
        for user in (None, self.regular, self.editor, self.owner):
            self.client.force_authenticate(user=user)
            response = self.client.get(self.list_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data[0]["id"], str(self.blog.id))
            self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
            self.assertEqual(self.client.head(self.list_url).status_code, status.HTTP_200_OK)

    def test_response_fields_and_no_account_data(self):
        self.blog.starred_by.add(self.regular)
        data = self.client.get(self.detail_url).data
        self.assertEqual(set(data), {
            "id", "title", "content", "read_time", "date_posted",
            "date_posted_display", "snippet", "star_count", "is_starred", "starred_by_names",
        })
        self.assertEqual(data["star_count"], 1)
        self.assertEqual(data["starred_by_names"], "regular")
        self.assertNotIn("email", str(data))
        self.assertNotIn("password", str(data))

    def test_search_by_title_and_empty_result(self):
        BlogPost.objects.create(title="Django notes", content="ORM", read_time=2)
        response = self.client.get(self.list_url, {"title": "HACKATHON"})
        self.assertEqual([item["title"] for item in response.data], ["Hackathon recap"])
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_missing_post_returns_404(self):
        url = reverse("api:blog-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.patch(url, {"title": "x"}, format="json").status_code, 404)
        self.assertEqual(self.client.delete(url).status_code, 404)
        star = reverse("api:blog-star", args=[uuid.uuid4()])
        self.assertEqual(self.client.post(star).status_code, status.HTTP_404_NOT_FOUND)

    def test_list_avoids_n_plus_one_queries(self):
        for i in range(5):
            post = BlogPost.objects.create(title=f"Post {i}", content="c", read_time=1)
            post.starred_by.add(self.regular, self.editor)
        # One query for posts, one prefetch for every post's stars
        with self.assertNumQueries(2):
            response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 6)

    # Visitor and regular user: read only

    def test_visitor_and_regular_user_cannot_write(self):
        for user in (None, self.regular):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Hacked"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertBlogUnchanged()

    # Editor: read, star, PUT/PATCH only

    def test_editor_can_patch_and_put(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"title": "Edited title"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.title, "Edited title")
        self.assertEqual(self.blog.content, "What I learned.")

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog.refresh_from_db()
        self.assertEqual((self.blog.title, self.blog.content, self.blog.read_time),
                         ("New post", "Fresh content", 5))

    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertBlogUnchanged()

    def test_staff_without_editor_permission_cannot_edit(self):
        self.regular.is_staff = True
        self.regular.save()
        self.client.force_authenticate(user=self.regular)
        response = self.client.patch(self.detail_url, {"title": "Hacked"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertBlogUnchanged()

    def test_put_requires_all_fields(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.put(self.detail_url, {"title": "Only title"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.data)
        self.assertBlogUnchanged()

    # Owner: everything

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = BlogPost.objects.get(pk=response.data["id"])
        self.assertEqual(created.title, "New post")
        self.assertIsNotNone(created.date_posted)

        response = self.client.patch(self.detail_url, {"read_time": 7}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.read_time, 7)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(BlogPost.objects.filter(pk=self.blog.id).exists())

    # Validation

    def test_invalid_input_returns_400(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": ""}, "title"),
            ({"title": "   "}, "title"),
            ({"title": "<b></b>"}, "title"),
            ({"content": "<p> </p><br>"}, "content"),
            ({"read_time": 0}, "read_time"),
            ({"read_time": -3}, "read_time"),
            ({"read_time": "abc"}, "read_time"),
            ({"title": "x" * 256}, "title"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, changes)
            self.assertIn(field, response.data)
        self.assertBlogUnchanged()

    def test_patch_validation_does_not_save(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"title": "<i></i>"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["title"], ["Post title can't contain only HTML tags."])
        self.assertBlogUnchanged()

    def test_html_tags_are_stripped(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "title": "<b>Bold</b> title", "content": "Hi <script>x</script>there",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = BlogPost.objects.get(pk=response.data["id"])
        self.assertEqual(created.title, "Bold title")
        self.assertNotIn("<script>", created.content)

    def test_malformed_json_returns_400(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, '{"title": ', content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertBlogUnchanged()

    def test_read_only_fields_cannot_be_set(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "id": str(self.blog.id), "date_posted": "2000-01-01",
            "star_count": 99, "is_starred": True, "starred_by_names": "forged",
            "starred_by": [self.regular.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data["id"], str(self.blog.id))
        self.assertNotEqual(response.data["date_posted"], "2000-01-01")
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertFalse(BlogPost.objects.get(pk=response.data["id"]).starred_by.exists())

    # Star

    def test_anonymous_cannot_star(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(self.blog.starred_by.exists())

    def test_every_logged_in_role_can_star_and_unstar(self):
        for user in (self.regular, self.editor, self.owner):
            self.client.force_authenticate(user=user)
            response = self.client.post(self.star_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data["is_starred"])
            self.assertTrue(self.blog.starred_by.filter(pk=user.pk).exists())
        self.assertEqual(self.blog.starred_by.count(), 3)

        self.client.force_authenticate(user=self.regular)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 2)
        self.assertFalse(self.blog.starred_by.filter(pk=self.regular.pk).exists())

    def test_star_uses_request_user_only(self):
        self.client.force_authenticate(user=self.regular)
        # A forged user id in the body is ignored
        response = self.client.post(self.star_url, {"user": self.owner.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(self.blog.starred_by.all()), [self.regular])

    def test_is_starred_is_per_user(self):
        self.blog.starred_by.add(self.regular)
        self.client.force_authenticate(user=self.regular)
        self.assertTrue(self.client.get(self.detail_url).data["is_starred"])
        self.client.force_authenticate(user=self.editor)
        self.assertFalse(self.client.get(self.detail_url).data["is_starred"])
        self.client.force_authenticate(user=None)
        self.assertFalse(self.client.get(self.detail_url).data["is_starred"])

    def test_wrong_methods_return_405(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # CSRF with a real session login

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="editor", password="test-password"))
        response = client.patch(self.detail_url, {"title": "No token"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertBlogUnchanged()
        self.assertFalse(self.blog.starred_by.exists())

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        # The Browsable API form puts a real CSRF cookie on the client
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 2)


class BlogHTMLRolesTest(APITestCase):
    """The old HTML blog views follow the same roles as the API."""

    def setUp(self):
        editor_group = Group.objects.create(name="Editor")
        editor_group.permissions.set(Permission.objects.filter(
            codename__in=["add_blogpost", "change_blogpost", "delete_blogpost"],
        ))
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(editor_group)
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.blog = BlogPost.objects.create(title="Recap", content="Text", read_time=2)
        self.form_data = {"title": "Added", "content": "Body", "read_time": 2}

    def test_editor_cannot_create_or_delete_through_html_views(self):
        self.client.login(username="editor", password="test-password")
        self.assertEqual(self.client.get(reverse("main:create_blog")).status_code, 403)
        self.assertEqual(self.client.post(reverse("main:create_blog"), self.form_data).status_code, 403)
        response = self.client.post(reverse("main:delete_blog", args=[self.blog.id]))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(list(BlogPost.objects.values_list("title", flat=True)), ["Recap"])

    def test_editor_can_still_use_html_update_view(self):
        self.client.login(username="editor", password="test-password")
        url = reverse("main:update_blog", args=[self.blog.id])
        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.post(url, {"title": "Edited", "content": "Text", "read_time": 2})
        self.assertRedirects(response, reverse("main:show_blog"))
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.title, "Edited")

    def test_owner_can_create_and_delete_through_html_views(self):
        self.client.login(username="owner", password="test-password")
        response = self.client.post(reverse("main:create_blog"), self.form_data)
        self.assertRedirects(response, reverse("main:show_blog"))
        response = self.client.post(reverse("main:delete_blog", args=[self.blog.id]))
        self.assertRedirects(response, reverse("main:show_blog"))
        self.assertEqual(list(BlogPost.objects.values_list("title", flat=True)), ["Added"])

    def test_removed_blog_endpoints_are_gone(self):
        # The DRF endpoints under /api/v1/blog/ replace these
        for name, args in [("get_blogs_json", []), ("create_blog_ajax", []),
                           ("toggle_star_blog", [self.blog.id])]:
            with self.assertRaises(NoReverseMatch):
                reverse(f"main:{name}", args=args)
        self.client.login(username="owner", password="test-password")
        self.assertEqual(self.client.get("/api/blog/").status_code, 404)
        self.assertEqual(self.client.post("/blog/add-ajax/", self.form_data).status_code, 404)
        self.assertEqual(BlogPost.objects.count(), 1)

    def test_blog_page_buttons_match_roles(self):
        self.client.login(username="editor", password="test-password")
        page = self.client.get(reverse("main:show_blog"))
        self.assertNotContains(page, 'id="blog-add-button"')
        self.assertContains(page, 'id="blog-form"')  # edit modal
        self.client.login(username="owner", password="test-password")
        page = self.client.get(reverse("main:show_blog"))
        self.assertContains(page, 'id="blog-add-button"')
