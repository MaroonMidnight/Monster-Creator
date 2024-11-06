from django.shortcuts import render, redirect
from .models import Monster, Moves
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.core.validators import MinValueValidator, MaxValueValidator

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
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Access the form field and set min and max attributes
        form.fields['attack'].widget.attrs.update({
            'min': 0,  # Set the minimum value
            'max': 10,  # Set the maximum value
        })
        form.fields['speed'].widget.attrs.update({
            'min': 0,  # Set the minimum value
            'max': 10,  # Set the maximum value
        })
        form.fields['defense'].widget.attrs.update({
            'min': 0,  # Set the minimum value
            'max': 10,  # Set the maximum value
        })

        return form

        
    def form_valid(self, form):
        # Access POST data
        attack_data = form.cleaned_data.get('attack') # x3
        speed_data = form.cleaned_data.get('speed')
        defense_data = form.cleaned_data.get('defense')
        # Perform operations with the data
        print(f"Received: {attack_data}") 
        
        total = attack_data + speed_data + defense_data
        
        if total > 10 or total < 10:
            # Add an error if the value is 10 or below
            form.add_error('attack', 'the sum of Attack, Speed and Defense must be equal to 10')
            return self.form_invalid(form)  # Re-render form with error message
        
        # Save the form and continue with the normal workflow
        return super().form_valid(form)

    
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