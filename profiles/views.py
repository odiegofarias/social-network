from django.shortcuts import render
from .models import Profile, Relationship

# Create your views here.
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
    }

    return render(request, 'profiles/myprofile.html', context)

def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invatations_received(profile)

    context = {
        'qs': qs,
    }

    return render(request, 'profiles/my_invites.html', context)

def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {
        'qs': qs,
    }

    return render(request, 'profiles/profile_list.html', context)

def invites_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {
        'qs': qs,
    }

    return render(request, 'profiles/to_invite_list.html', context)
