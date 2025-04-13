from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .models import Poll, Choice, Vote
from .serializers import PollSerializer, ChoiceSerializer
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'index.html')

def create_poll(request):
    if request.method == 'POST':
        question = request.POST['question']
        choice1 = request.POST['choice1']
        choice2 = request.POST['choice2']
        choice3 = request.POST.get('choice3', '')

        poll = Poll.objects.create(question=question)

        Choice.objects.create(poll=poll, choice_text=choice1)
        Choice.objects.create(poll=poll, choice_text=choice2)
        if choice3:
            Choice.objects.create(poll=poll, choice_text=choice3)

        return redirect('/')
    return render(request, 'create.html')

def vote(request, poll_id, choice_id):
    # Get the poll and choice
    poll = get_object_or_404(Poll, id=poll_id)
    choice = get_object_or_404(Choice, id=choice_id, poll=poll)

    # Check if the user has already voted for this poll/choice in the session
    if request.session.get(f'voted_{poll_id}_{choice_id}', False):
        return JsonResponse({'error': 'You have already voted in this poll.'}, status=400)

    # Create a new vote record
    Vote.objects.create(choice=choice)

    # Increment the vote count for the choice
    choice.votes += 1
    choice.save()

    # Mark the session to prevent further voting for this poll/choice
    request.session[f'voted_{poll_id}_{choice_id}'] = True

    return JsonResponse({'message': 'Your vote has been recorded successfully!'})

class PollListCreateView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollDetailView(generics.RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class VoteView(APIView):
    def post(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        choice_id = request.data.get("choice_id")

        # Check if the choice exists in the poll
        try:
            choice = poll.choices.get(id=choice_id)
        except Choice.DoesNotExist:
            return Response({"error": "Invalid choice"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has already voted (session-based tracking)
        if request.session.get(f'voted_{poll.id}_{choice.id}', False):
            return Response({"error": "You have already voted in this poll."}, status=status.HTTP_400_BAD_REQUEST)

        # Increment the vote count for the choice
        choice.votes += 1
        choice.save()

        # Mark the session to prevent further voting for this poll/choice
        request.session[f'voted_{poll.id}_{choice.id}'] = True

        return Response({"message": "Vote recorded!"})

class PollResultsView(APIView):
    def get(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        choices = poll.choices.all()
        data = ChoiceSerializer(choices, many=True).data
        return Response(data)

def vote_choice(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    choice.votes += 1
    choice.save()
    Vote.objects.create(choice=choice)
    return redirect('polls')


@csrf_exempt  # Disable CSRF for testing from Postman
def vote_choice_api(request, choice_id):
    if request.method == 'POST':
        choice = get_object_or_404(Choice, id=choice_id)
        choice.votes += 1
        choice.save()
        Vote.objects.create(choice=choice)
        return JsonResponse({'message': 'Vote recorded successfully', 'choice': choice.choice_text, 'votes': choice.votes})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)