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
            return redirect('mashamba:farm_detail', slug=farm.slug)
    else:
        form = FarmForm()
    return render(request, 'mashamba/dairyfarm/register_farm.html', {'form': form})


@login_required
def farm_list_view(request):
    user = request.user
    farms = Farm.objects.filter(manager=user)  # Filter farms by current user
    context = {
        'farms': farms
    }
    return render(request, 'mashamba/dairyfarm/farm_list.html', context)


@login_required
def farm_detail_view(request, slug):
    farm = get_object_or_404(Farm, slug=slug)
    context = {
        'farm': farm,
    }
    return render(request, 'mashamba/dairyfarm/farm_detail.html', context)

@login_required
def cow_list_view(request, slug):
    user = request.user
    farm = get_object_or_404(Farm, slug=slug, manager=user)  # Ensure user owns the farm
    cows = Cow.objects.filter(farm=farm)
    
    context = {
        'farm': farm,
        'cows': cows,
    }
    return render(request, 'mashamba/dairyfarm/cow_list.html', context)


@login_required
def cow_detail_view(request, slug, cow_id):
    user = request.user
    farm = get_object_or_404(Farm, slug=slug, manager=user)  # Ensure user owns the farm
    cow = get_object_or_404(Cow, id=cow_id, farm=farm)
    last_mass = cow.mass_measurements.order_by('-date_measured').first()

    context = {
        'farm': farm,
        'cow': cow,
        'last_mass': last_mass
    }
    return render(request, 'mashamba/dairyfarm/cow_detail.html', context)


@login_required
def milking_sessions_view(request, slug, cow_id):
    user = request.user
    farm = get_object_or_404(Farm, slug=slug, manager=user)  # Ensure user owns the farm
    cow = get_object_or_404(Cow, id=cow_id, farm=farm)
    milking_sessions = MilkingSession.objects.filter(cow=cow).order_by('-milking_time')

    context = {
        'farm': farm,
        'cow': cow,
        'milking_sessions': milking_sessions,
    }

    return render(request, 'mashamba/dairyfarm/milking_sessions.html', context)


@login_required
def all_cows_milk_view(request, slug):
    user = request.user
    farm = get_object_or_404(Farm, slug=slug, manager=user)  # Ensure user owns the farm
    milking_sessions = MilkingSession.objects.filter(cow__farm=farm).order_by('-milking_time')

    context = {
        'farm': farm,
        'milking_sessions': milking_sessions,
    }
    return render(request, 'mashamba/dairyfarm/all_cows_milk.html', context)
