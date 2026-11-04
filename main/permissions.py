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
