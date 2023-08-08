from django.db import models

class EventGamer(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="gamer_relationships")
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name="event_relationships")
