import datetime
import random

from django.db import models
from homePage.models import *
from django.utils import timezone

# Create your models here.
class RandomCode(models.Model) :
    value = models.BigIntegerField(default=random.randint(1_000_000 , 9_999_999))
    related_to = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
         if timezone.now() - self.created_at > datetime.timedelta(minutes=2) : return False
         else : return True