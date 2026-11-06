from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can change projects."

    # The owner is the superuser. IsAdminUser would check is_staff instead,
    # and the Editor group's model permissions don't apply to this API.
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """
    Blog API roles from Assignment 4:
    - visitor / regular user: read only (GET, HEAD, OPTIONS)
    - Editor (has main.change_blogpost): read + PUT/PATCH
    - portfolio owner (superuser): everything, including POST and DELETE
    """

    message = "You don't have permission to do this to blog posts."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if request.method in ("PUT", "PATCH"):
            return user.has_perm("main.change_blogpost")
        return False
