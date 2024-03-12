from django.db import models

def default_board_state():
    return [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

class GameSession(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    player1 = models.CharField(max_length=50)
    player2 = models.CharField(max_length=50)
    board_state = models.JSONField(default=default_board_state)
    active = models.BooleanField(default=True)
    last_move = models.CharField(max_length=1, default=' ')

    def __str__(self):
        return self.session_id
