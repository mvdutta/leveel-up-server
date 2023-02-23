from django.db import models

class GamerEvent(models.Model):

    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='registered_gamers')
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='event_registrations')
