from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=55)
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name="created_events")
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="events_for_game")
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    attendees = models.ManyToManyField("Gamer", through='EventGamer')
