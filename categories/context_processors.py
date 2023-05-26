"""
context_processors is a list of dotted Python paths to callables that are used to
populate the context when a template is rendered with a request.
These callables take a request object as their argument and return a dict of items
to be merged into the context.
https://docs.djangoproject.com/en/4.2/ref/templates/api/#built-in-template-context-processors


A context processor has a simple interface: it’s a Python function that takes one argument,
an HttpRequest object, and returns a dictionary that gets added to the template context.
Each context processor must return a dictionary.
https://betterprogramming.pub/django-quick-tips-context-processors-da74f887f1fc
"""

from .models import Category


def menu_links(request):
    return {
        "all_categories": Category.objects.all(),
    }
