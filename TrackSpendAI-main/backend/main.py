"""Convenience entrypoint for the backend.

Usage:
  python main.py                # runs Django dev server on 8000
  python main.py runserver 0.0.0.0:8000  # pass-through to Django manage command

This file sets DJANGO_SETTINGS_MODULE and delegates to Django's
`execute_from_command_line` so `python main.py` works like `manage.py`.
"""
import os
import sys
from pathlib import Path

# Ensure project root is on PYTHONPATH so imports work when running from any cwd
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# Default DJANGO_SETTINGS_MODULE (matches project layout)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "item_service.settings")

try:
    import django
    from django.core.management import execute_from_command_line
except Exception as e:
    print("Failed to import Django. Make sure your virtualenv is activated and dependencies are installed.")
    print("Error:", e)
    sys.exit(1)


def main():
    # If no args passed, run the development server
    args = sys.argv
    if len(args) == 1:
        args = [args[0], "runserver", "8000"]

    try:
        execute_from_command_line(args)
    except Exception as e:
        print("Error executing Django command:", e)
        raise


if __name__ == "__main__":
    main()
