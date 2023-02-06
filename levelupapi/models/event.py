from django.db import models


class Event(models.Model):

    attendee = models.ManyToManyField("Gamer", through="GamerEvent", related_name='attending_event')
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='game_event')
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='event_organizer')
    event_date = models.DateField(auto_now=False, auto_now_add=False)
    event_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    description = models.CharField(max_length=155)

