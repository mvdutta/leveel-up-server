class Gamer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
