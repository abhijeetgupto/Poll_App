from django.urls import path
from .views import CustomLoginView, RegisterUser, ListPoll, PollDetail, PollResult, CreatePoll, UserProfile

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name='login-page'),
    path("logout/", LogoutView.as_view(next_page='login-page'), name='logout'),
    path("register/", RegisterUser.as_view(), name='register-page'),
    path("", ListPoll.as_view(), name='list-polls'),
    path("poll-detail/<pk>", PollDetail, name='poll-detail'),
    path("poll-result/<pk>", PollResult, name='poll-result'),
    path("create-poll/", CreatePoll.as_view(), name='create-poll'),
    path("user-profile/", UserProfile, name='user-profile'),

]
