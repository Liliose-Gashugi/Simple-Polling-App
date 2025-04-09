from django.urls import path
from .views import PollListCreateView, PollDetailView, VoteView, PollResultsView
from polls.views import home, create_poll

urlpatterns = [
    path('polls/', PollListCreateView.as_view(), name='poll-list'),
    path('polls/<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
    path('polls/<int:pk>/vote/', VoteView.as_view(), name='poll-vote'),
    path('polls/<int:pk>/results/', PollResultsView.as_view(), name='poll-results'),
]
