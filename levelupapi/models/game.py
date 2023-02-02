from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Game(models.Model):

    game_title = models.CharField(max_length=100)
    type = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name='game_type')
    creator = models.ForeignKey("Gamer", null=True, blank=True, on_delete=models.CASCADE, related_name='game_creator')
    skill_level = models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(1)])
    maker = models.CharField(max_length=50)
    num_of_players = models.IntegerField(validators=MinValueValidator(1))
