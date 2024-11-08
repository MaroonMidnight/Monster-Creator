from django.shortcuts import render, redirect
from .models import Monster, Moves
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('monster-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)


class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')



class MonsterList(LoginRequiredMixin,ListView):
    model = Monster

    def get_queryset(self):
        # Filter the queryset to show only objects related to the logged-in user
        return Monster.objects.filter(user=self.request.user)

@login_required
def monster_detail(request, monster_id):
    monster = Monster.objects.get(id=monster_id)
    moves_monster_doesnt_have = Moves.objects.filter(user=request.user).exclude(id__in = monster.moves.all().values_list('id'))
    return render(request, 'monsters/detail.html', {'monster': monster, 'moves': moves_monster_doesnt_have,})


class MonsterCreate(LoginRequiredMixin,CreateView):
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
        
        if total > 10:
            # Add an error if the value is 10 or below
            form.add_error('attack', 'the sum of Attack, Speed and Defense must be equal to 10')
            return self.form_invalid(form)  # Re-render form with error message
        form.instance.user = self.request.user
        # Save the form and continue with the normal workflow
        return super().form_valid(form)
    
    

class MonsterUpdate(LoginRequiredMixin,UpdateView):
    model = Monster
    fields = ['name', 'species', 'color', 'passive', 'attack', 'speed', 'defense']
  
 
class MonsterDelete(LoginRequiredMixin,DeleteView):
    model = Monster
    success_url = '/monsters'
    
 
class MovesCreate(LoginRequiredMixin,CreateView):
    model = Moves
    fields = ['move_effect', 'special']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

@login_required
def add_moves(request, monster_id):
    form = Moves(request.POST)
    
    if form.is_valid():
        new_moves = form.save(commit=False)
        new_moves.monster_id = monster_id
        new_moves.save()
    return redirect('monster-detail', monster_id=monster_id)
    
class MovesDetail(LoginRequiredMixin,DetailView):
    model = Moves
     
class MovesList(LoginRequiredMixin,ListView):
    model = Moves
    fields = '__all__'
    
    def get_queryset(self):
        # Filter the queryset to show only objects related to the logged-in user
        return Moves.objects.filter(user=self.request.user)

class MovesUpdate(LoginRequiredMixin,UpdateView):
    model = Moves
    fields = ['move_effect', 'special']

class MovesDelete(LoginRequiredMixin,DeleteView):
    model = Moves
    success_url = '/moves'
    
def associate_moves(request, monster_id, moves_id):
    Monster.objects.get(id=monster_id).moves.add(moves_id)
    return redirect('monster-detail', monster_id=monster_id)

@login_required
def remove_moves(request, monster_id, moves_id):
    monster = Monster.objects.get(id=monster_id)
    moves = Moves.objects.get(id=moves_id)
    monster.moves.remove(moves)
    
    return redirect('monster-detail', monster_id=monster.id)