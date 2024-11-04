from django.shortcuts import render, redirect
from .models import Monster, Moves
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class MonsterList(ListView):
    model = Monster

def monster_detail(request, monster_id):
    monster = Monster.objects.get(id=monster_id)
    moves_monster_doesnt_have = Moves.objects.exclude(id__in = monster.moves.all().values_list('id'))
    return render(request, 'monsters/detail.html', {'monster': monster, 'moves': moves_monster_doesnt_have,})

class MonsterCreate(CreateView):
    model = Monster
    fields = ['name', 'species', 'color', 'passive', 'attack', 'speed', 'defense']
    
class MonsterUpdate(UpdateView):
    model = Monster
    fields = ['name', 'species', 'color', 'passive', 'attack', 'speed', 'defense']
    
class MonsterDelete(DeleteView):
    model = Monster
    success_url = '/monsters'
    
class MovesCreate(CreateView):
    model = Moves
    fields = '__all__'

def add_moves(request, monster_id):
    form = Moves(request.POST)
    
    if form.is_valid():
        new_moves = form.save(commit=False)
        new_moves.monster_id = monster_id
        new_moves.save()
    return redirect('monster-detail', monster_id=monster_id)
    
class MovesDetail(DetailView):
    model = Moves
    
class MovesList(ListView):
    model = Moves
    fields = '__all__'

class MovesUpdate(UpdateView):
    model = Moves
    fields = '__all__'
    
class MovesDelete(DeleteView):
    model = Moves
    success_url = '/moves'
    
def associate_moves(request, monster_id, moves_id):
    Monster.objects.get(id=monster_id).moves.add(moves_id)
    return redirect('monster-detail', monster_id=monster_id)

def remove_moves(request, monster_id, moves_id):
    monster = Monster.objects.get(id=monster_id)
    moves = Moves.objects.get(id=moves_id)
    monster.moves.remove(moves)
    
    return redirect('monster-detail', monster_id=monster.id)