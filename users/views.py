from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, render

from .forms import CreationForm
from recipe.models import User


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'reg.html'
