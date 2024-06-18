# views.py

from django.shortcuts import render, get_object_or_404
from .models import Farm

def farm_detail_view(request, slug):
    farm = get_object_or_404(Farm, slug=slug)
    context = {
        'farm': farm,
    }
    return render(request, 'farm_detail.html', context)
