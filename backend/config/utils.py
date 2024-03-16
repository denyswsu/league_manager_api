import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name, default=None):
    """Get the environment variable or return exception if not found or empty"""
    value = os.environ.get(var_name, default)
    if not value:
        error_msg = f"Set the {var_name} environment variable with a non-empty value"
        raise ImproperlyConfigured(error_msg)

    return value
