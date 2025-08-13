from functools import wraps
# from users.serializers import IsSuperUser
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

# TODO; Fix authentication - dont AllowAny


def decorator_accounts(view_func):
    """Custom decorator to combine multiple DRF decorators."""

    @api_view(['GET', 'POST'])
    @permission_classes([AllowAny])
    @authentication_classes([])
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def decorator_account_detail(view_func):
    """Custom decorator to combine multiple DRF decorators."""

    @api_view(['GET', 'PATCH', 'DELETE'])
    @permission_classes([AllowAny])
    @authentication_classes([])
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def decorator_overview(view_func):
    """Custom decorator to combine multiple DRF decorators."""
    @api_view(['GET'])
    @permission_classes([AllowAny])
    @authentication_classes([])
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped_view
