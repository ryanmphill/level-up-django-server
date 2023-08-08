from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=55)
    game_type = models.ForeignKey("GameType", null=True, on_delete=models.SET_NULL, related_name="included_games")
    creator = models.ForeignKey("Gamer", null=True, on_delete=models.SET_NULL, related_name="created_games")
    