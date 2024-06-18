# views.py
from django.shortcuts import render, get_object_or_404
from .models import Cow, Farm, MilkingSession
from collections import defaultdict
from django.db.models import DateField
from django.db.models.functions import Cast


def farm_detail_view(request, slug):
    farm = get_object_or_404(Farm, slug=slug)
    context = {
        'farm': farm,
    }
    return render(request, 'farm_detail.html', context)


def cow_list_view(request, slug):
    farm = get_object_or_404(Farm, slug=slug)
    cows = Cow.objects.filter(farm=farm)  # Assuming a ForeignKey from Cow to Farm
    context = {
        'farm': farm,
        'cows': cows,
    }
    return render(request, 'cow_list.html', context)

def cow_detail_view(request, slug, cow_id):
    farm = get_object_or_404(Farm, slug=slug)
    cow = get_object_or_404(Cow, id=cow_id, farm=farm)
    last_mass = cow.mass_measurements.order_by('-date_measured').first()
    
    context = {
        'farm': farm,
        'cow': cow,
        'last_mass': last_mass
    }
    return render(request, 'cow_detail.html', context)

def milking_sessions_view(request, slug, cow_id):
    farm = get_object_or_404(Farm, slug=slug)
    cow = get_object_or_404(Cow, id=cow_id, farm=farm)
    milking_sessions = MilkingSession.objects.filter(cow=cow).order_by('-milking_time')

    context = {
        'farm': farm,
        'cow': cow,
        'milking_sessions': milking_sessions,
    }

    return render(request, 'milking_sessions.html', context)


def all_cows_milk_view(request, slug):
    farm = get_object_or_404(Farm, slug=slug)
    milking_sessions = MilkingSession.objects.filter(cow__farm=farm).order_by('-milking_time')

    context = {
        'farm': farm,
        'milking_sessions': milking_sessions,
    }
    return render(request, 'all_cows_milk.html', context)
