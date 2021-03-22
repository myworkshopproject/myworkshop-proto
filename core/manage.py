#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            os.environ.setdefault(key, value)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
