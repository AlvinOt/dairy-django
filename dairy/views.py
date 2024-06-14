from django.shortcuts import render, get_object_or_404
from .models import Farm, Status

def farm_list(request):
    farms = Farm.activated.all()
    return render(request,
                 'dairy/farm/list.html',
                 {'farms': farms})


def farm_detail(request, id):
    farm = get_object_or_404(Farm,
                             id=id,
                             status=Status.ACTIVE)
    return render(request,
                  'dairy/farm/detail.html',
                  {'farm': farm})
