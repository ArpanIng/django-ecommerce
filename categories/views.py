from django.http import HttpResponse
from django.shortcuts import render

from .models import Category


def category_list(request):
    return HttpResponse("Category")
