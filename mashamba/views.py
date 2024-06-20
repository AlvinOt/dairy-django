# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cow, Farm, MilkingSession
from django.db.models import DateField
from .forms import FarmForm
from django.contrib.auth.decorators import login_required

def home_view(request):
    return render(request, 'mashamba/dairyfarm/home.html')


@login_required
def dashboard_view(request):
    user = request.user
    farms = Farm.objects.filter(manager=user)
    return render(request, 'mashamba/dairyfarm/dashboard.html', {'farms': farms})


@login_required
def register_farm_view(request):
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.manager = request.user
            farm.save()
            return redirect('farm_detail', slug=farm.slug)
    else:
        form = FarmForm()
    return render(request, 'mashamba/dairyfarm/register_farm.html', {'form': form})

def farm_list_view(request):
    farms = Farm.objects.all()
    context = {
            'farms': farms
            }
    return render(request,
            'mashamba/dairyfarm/farm_list.html', context)

def farm_detail_view(request, slug):
    farm = get_object_or_404(Farm, slug=slug)
    context = {
        'farm': farm,
    }
    return render(request, 'mashamba/dairyfarm/farm_detail.html', context)


def cow_list_view(request, slug):
    farm = get_object_or_404(Farm, slug=slug)
    cows = Cow.objects.filter(farm=farm)  # Assuming a ForeignKey from Cow to Farm
    context = {
        'farm': farm,
        'cows': cows,
    }
    return render(request, 'mashamba/cow_list.html', context)

def cow_detail_view(request, slug, cow_id):
    farm = get_object_or_404(Farm, slug=slug)
    cow = get_object_or_404(Cow, id=cow_id, farm=farm)
    last_mass = cow.mass_measurements.order_by('-date_measured').first()
    
    context = {
        'farm': farm,
        'cow': cow,
        'last_mass': last_mass
    }
    return render(request, 'mashamba/cow_detail.html', context)

def milking_sessions_view(request, slug, cow_id):
    farm = get_object_or_404(Farm, slug=slug)
    cow = get_object_or_404(Cow, id=cow_id, farm=farm)
    milking_sessions = MilkingSession.objects.filter(cow=cow).order_by('-milking_time')

    context = {
        'farm': farm,
        'cow': cow,
        'milking_sessions': milking_sessions,
    }

    return render(request, 'mashamba/milking_sessions.html', context)


def all_cows_milk_view(request, slug):
    farm = get_object_or_404(Farm, slug=slug)
    milking_sessions = MilkingSession.objects.filter(cow__farm=farm).order_by('-milking_time')

    context = {
        'farm': farm,
        'milking_sessions': milking_sessions,
    }
    return render(request, 'mashamba/all_cows_milk.html', context)
