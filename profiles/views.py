
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm
from checkout.models import Order


def profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    template = 'profiles/profile.html'

    context = {
        'profile' :profile,
    }
    return render(request, template, context)