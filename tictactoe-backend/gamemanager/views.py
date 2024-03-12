
import uuid
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import GameSession


def generate_session_id():
    return uuid.uuid4()

class RegisterForGame(APIView):
    def post(self, request, username):
        available_board = GameSession.objects.filter(player2='')
        if available_board.exists():
            game_session = available_board.first()
            game_session.player2 = username
            game_session.save()
            session_id = game_session.session_id
            return JsonResponse({"session_id": session_id}, status=200)
        else:
            session_id = generate_session_id()
            GameSession.objects.create(session_id = session_id, player1 = username)
            return  JsonResponse({'session_id': session_id}, status=200)

