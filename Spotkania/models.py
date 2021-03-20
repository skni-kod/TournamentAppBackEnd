from django.db import models
from Api.models import *
from django.core.validators import MinValueValidator, MaxValueValidator

class Meet(models.Model):

    id_meet = models.IntegerField(primary_key=True)
    id_player = models.ForeignKey(Player,on_delete=models.CASCADE,related_name='+')
    id_player1 = models.ForeignKey(Player,on_delete=models.CASCADE,related_name='+')
    result = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(1)])
    date = models.DateTimeField()
    round = models.IntegerField()


