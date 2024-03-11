from django.db import models

class GameSession(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    player1 = models.CharField(max_length=50)
    player2 = models.CharField(max_length=50)
    board_state = models.JSONField(default=list)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.session_id
