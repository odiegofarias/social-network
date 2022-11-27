from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
    path('myprofile/', views.my_profile_view, name='my-profile-view'),
    path('my-invites/', views.invites_received_view, name='my-invites-view'),
    path('', views.ProfileListView.as_view(), name='all-profiles-view'),
    path('to-invite/', views.invites_profiles_list_view,
         name='invites-profile-view'),
    path('send-invite/', views.send_invitation, name='send-invite'),
    path('remove-friend/', views.remove_from_friends, name='remove-friend'),
    path('my-invites/accepted/', views.accept_invitation, name='accept-invite'),
    path('my-invites/rejected/', views.reject_invitation, name='reject-invite'),
    path('<slug>/', views.ProfileDetailView.as_view(), name='profile-detail-view'),
    path('register/', views.register_form_view, name='register'),
]
