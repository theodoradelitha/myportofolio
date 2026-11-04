from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack",
            "demo_link", "image",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]
        # A blank image falls back to the folder icon in validate_image
        extra_kwargs = {"image": {"allow_blank": True}}

    # ProjectForm's clean_* methods don't run for API requests,
    # so the same cleaning rules are repeated here.
    def validate_title(self, value):
        title = strip_tags(value).strip()
        if not title:
            raise serializers.ValidationError("Project name can't contain only HTML tags.")
        return title

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate_tech_stack(self, value):
        return strip_tags(value).strip()

    def validate_image(self, value):
        image = strip_tags(value).strip()
        return image or Project._meta.get_field("image").default

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())
