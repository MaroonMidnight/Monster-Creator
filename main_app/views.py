from django.shortcuts import render
from .models import Monster
from django.views.generic.edit import CreateView


# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def monster_index(request):
    monster = Monster.objects.all()
    return render(request, 'monster/index.html', {'monster': monster})

def monster_detail(request, monster_id):
    monster = Monster.objects.get(id=monster_id)
    return render(request, 'monsters/detail.html', {'monster': monster})

class MonsterCreate(CreateView):
    model = Monster
    fields = ['name', 'species', 'color', 'passive', 'attack', 'speed', 'defense']