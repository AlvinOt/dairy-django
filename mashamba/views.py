# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cow, Farm, MilkingSession
from django.db.models import DateField
from .forms import FarmForm
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.db.models import Prefetch
from django.http import HttpResponseForbidden


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def home_view(request):
    return render(request, 'mashamba/dairyfarm/index.html')


"""
@login_required
def dashboard_view(request):
    user = request.user
    farms = Farm.objects.filter(manager=user)
    return render(request, 'mashamba/dairyfarm/dashboard.html', {'farms': farms})
"""

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
def all_farms_view(request):
    user = request.user
    user_farms = Farm.objects.filter(manager=user)
    other_farms = Farm.objects.exclude(manager=user)
    context = {
        'user_farms': user_farms,
        'other_farms': other_farms
    }
    return render(request, 'mashamba/dairyfarm/all_farms.html', context)


@login_required
def farm_list_view(request):
    user = request.user
    farms = Farm.objects.filter(manager=user)  # Filter farms by current user
    context = {
        'farms': farms
    }
    return render(request, 'mashamba/dairyfarm/farm_list.html', context)


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
    grouped_milk_yield = {}

    for session in milking_sessions:
        date = session.milking_time.date()
        if date not in grouped_milk_yield:
            grouped_milk_yield[date] = []
        grouped_milk_yield[date].append(session)

    sorted_grouped_milk_yield = dict(sorted(grouped_milk_yield.items(), reverse=True))

    context = {
        'cow': cow,
        'sorted_grouped_milk_yield': sorted_grouped_milk_yield,
        }
    return render(request, 'mashamba/dairyfarm/milking_sessions.html', context)


@login_required
def all_cows_milk_view(request, slug):
    user = request.user
    farm = get_object_or_404(Farm, slug=slug, manager=user)  # Ensure user owns the farm

    # Use Prefetch to optimize related data retrieval
    milking_sessions = MilkingSession.objects.filter(cow__farm=farm).select_related('cow').order_by('-milking_time')

    # Group milking sessions by cow and then by date
    grouped_milk_yield = defaultdict(lambda: defaultdict(list))
    for session in milking_sessions:
        date_str = session.milking_time.strftime("%Y-%m-%d")
        grouped_milk_yield[session.cow.name_or_tag][date_str].append(session)

    # Sort dates within each cow's group
    sorted_grouped_milk_yield = {cow: dict(sorted(sessions.items(), reverse=True)) for cow, sessions in grouped_milk_yield.items()}

    context = {
        'farm': farm,
        'milking_sessions': milking_sessions,
        'sorted_grouped_milk_yield': sorted_grouped_milk_yield,
    }
    return render(request, 'mashamba/dairyfarm/all_cows_milk.html', context)
