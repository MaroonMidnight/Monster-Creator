from django.db import models

from django.urls import reverse
# Create your models here.

SPECIES = (
    ('D', 'Dog'),
    ('C', 'Cat'),
    ('D', 'Dragon'),
    ('O', 'Ogre'),
    ('F', 'Fairy'),
    ('FI', 'Fish'),
    ('S', 'Slime'),
)

PASSIVE = (
    ('S', 'Sleepy'), # +1 defense -1 speed
    ('F', 'Fury'), # +1 attack -1 defense
    ('N', 'Nimble') # +1 speed -1 attack
)

SPECIALS = (
    ('P', 'Punch'),       
    ('K', 'Kick'),       
    ('S', 'Suffocation'),       
    ('F', 'Fire Claw'),       
    ('W', 'Wet Body'),       
    ('SH', 'Shadow Ball'),       
    ('FB', 'Fire Ball'),       
    ('H', 'Holy'),       
    ('G', 'Grass Knot'),       
    ('S', 'Slam'),       
)

class Moves(models.Model):
    move_effect = models.CharField(max_length=50)
    special = models.CharField(
        max_length=2,
        choices=SPECIALS,
        default=SPECIALS[0][0]
        )
    
    def __str__(self):
        return self.special
    
    def get_absolute_url(self):
        return reverse("moves-detail", kwargs={"pk": self.id})
    
    
    
class Monster(models.Model):
    name = models.CharField(max_length=20)
    species = models.CharField(
        max_length=2,
        choices = SPECIES,
        default = SPECIES[0][0]
        )
    color = models.CharField(max_length=20)
    passive = models.CharField(
        max_length=1,
        choices = PASSIVE,)
    attack = models.IntegerField(default=0)
    defense =  models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    
    moves = models.ManyToManyField(Moves)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("monster-detail", kwargs={"monster_id": self.id})
    
    
    
# class Passive(models.Model):
#     passive_description = models.CharField(max_length=50)
#     passives = models.CharField(
#         max_length=1,
#         choices = PASSIVE,
#     )
    
#     monster = models.ForeignKey(Monster, on_delete=models.CASCADE)