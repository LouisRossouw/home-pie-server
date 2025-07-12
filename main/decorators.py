from functools import wraps
# from users.serializers import IsSuperUser
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes


def decorator_admin_stats(view_func):
    """Custom decorator to combine multiple DRF decorators."""
    @api_view(['GET'])
    # @permission_classes([IsSuperUser])
    @permission_classes([IsAuthenticated])
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def decorator_stats(view_func):
    """Custom decorator to combine multiple DRF decorators."""
    @api_view(['GET'])
    @permission_classes([AllowAny])
    @authentication_classes([])  # Need this for anonymous users
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def decorator_health(view_func):
    """Custom decorator to combine multiple DRF decorators."""
    @api_view(['GET'])
    @permission_classes([AllowAny])
    @authentication_classes([])
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def decorator_test_view(view_func):
    """Custom decorator to combine multiple DRF decorators."""
    @api_view(['GET'])
    @permission_classes([AllowAny])
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def decorator_home_view(view_func):
    """Custom decorator to combine multiple DRF decorators."""
    @api_view(['GET'])
    @permission_classes([AllowAny])
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped_view
