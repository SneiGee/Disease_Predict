from django.db.models import Q
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages

from .forms import SignUpForm, UserForm, ProfileForm
from .models import Doctor


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the error")

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('my_account')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'my_account.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'nbar': 'userprofile'
    })


@method_decorator(login_required, name='dispatch')
class DoctorListView(ListView):
    template_name = 'doctor.html'

    def get(self, request):
        doctors = Doctor.objects.all()
        args = {'nbar': 'doctor', 'doctors': doctors}
        return render(request, self.template_name, args)


@login_required
def doctor_search(request):
    doctor = Doctor.objects.all()
    query = request.GET.get('q')
    if query:
        doctor = doctor.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(position__icontains=query)
        ).distinct()
    args = {'doctor': doctor, 'nbar': 'doctor'}
    return render(request, 'doctor_search.html', args)
