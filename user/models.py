from django.db import models
from django.db.models.fields import CharField, PositiveBigIntegerField, PositiveIntegerField
from django.db.models.fields.related import ForeignKey
from utils.models import nb
from tgbot import dispatcher
# Create your models here.

class User(models.Model):
    tg_id = PositiveBigIntegerField(unique=True)
    num_right = PositiveIntegerField(default=0)
    num_wrong = PositiveIntegerField(default=0)
    tag = CharField(max_length=300, **nb)

    @property
    def full_name(self):
        return dispatcher.bot.get_chat(self.tg_id).full_name
    
    @property
    def link(self):
        return dispatcher.bot.get_chat(self.tg_id).link
    
    def __str__(self):
        return self.full_name
    

class Answer(models.Model):
    user = ForeignKey(User, models.CASCADE)
    right_answer = CharField(max_length=3)
    answer = CharField(max_length=4, **nb)
    equasion = CharField(max_length=100, **nb)


    