from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
    path('myprofile/', views.my_profile_view, name='my-profile-view'),
    path('my-invites/', views.invites_received_view, name='my-invites-view'),
    path('all-profiles/', views.ProfileListView.as_view(), name='all-profiles-view'),
    path('to-invite/', views.invites_profiles_list_view, name='invites-profile-view'),
    path('send-invite/', views.send_invatation, name='send-invite'),
    path('remove-friend/', views.remove_from_friends, name='remove-friend'),
]
