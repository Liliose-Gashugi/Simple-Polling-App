from django.urls import path
from .views import PollListCreateView, PollDetailView, VoteView, PollResultsView
from polls.views import home, create_poll
from . import views

urlpatterns = [
    path('polls/', PollListCreateView.as_view(), name='poll-list'),
    path('polls/<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
    path('polls/<int:pk>/results/', PollResultsView.as_view(), name='poll-results'),
    # path('polls/<int:poll_id>/vote/<int:choice_id>/', views.vote, name='vote'),
    path('vote/<int:choice_id>/', views.vote_choice, name='vote_choice'),
    path('api/vote/<int:choice_id>/', views.vote_choice_api, name='vote_choice_api'),
]
