from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UserForm, ProfileForm, RoleFormSet
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
from .models import Profile

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'auth/signup.html', {'form': form})

def home(request):
    return render(request, 'home/index.html')

def user_is_admin(user):
    return user.profile.isAdmin()

def user_is_staff(user):
    output = user.profile.isStaff() or user.profile.isAdmin()
    return output

@login_required
@user_passes_test(user_is_admin)
def users_profile(request):
    if request.method == 'POST':
        profile_form = RoleFormSet(data=request.POST)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('home')

    else:
        profiles = Profile.objects.all()
        formset = RoleFormSet(queryset=profiles)

    return render(request, 'auth/users_profile.html', {'formset':formset, 'profiles': profiles})

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    profile = request.user.profile

    return render(request, 'auth/my_account.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile':profile
    })

@login_required
@user_passes_test(user_is_admin)
def user_profile(request, profile_id):
    profile = Profile.objects.filter(id=profile_id).first()
    return render(request, 'auth/user_profile.html', {
        'profile':profile
    })
