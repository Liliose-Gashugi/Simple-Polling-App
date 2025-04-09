from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer

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
        try:
            choice = poll.choices.get(id=choice_id)
        except Choice.DoesNotExist:
            return Response({"error": "Invalid choice"}, status=status.HTTP_400_BAD_REQUEST)
        choice.votes += 1
        choice.save()
        return Response({"message": "Vote recorded!"})

class PollResultsView(APIView):
    def get(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        choices = poll.choices.all()
        data = ChoiceSerializer(choices, many=True).data
        return Response(data)
