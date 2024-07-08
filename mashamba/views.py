# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cow, Farm, MilkingSession
from django.db.models import DateField, Sum
from .forms import UserRegistrationForm, FarmSubscriptionForm, CowForm, MilkingSessionForm
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.db.models import Prefetch
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def home_view(request):
    return render(request, 'mashamba/dairyfarm/index.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'mashamba/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request, 'mashamba/register.html', {'user_form': user_form})


@login_required
def subscribe_farm(request):
    if request.method == 'POST':
        form = FarmSubscriptionForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.manager = request.user
            farm.active = False
            farm.save()
            return redirect('mashamba:pay_to_activate', slug=farm.slug)
    else:
        form = FarmSubscriptionForm()
    return render(request, 'mashamba/dairyfarm/farm_subscription.html', {'form': form})


@login_required
def pay_to_activate_view(request, slug):
    farm = get_object_or_404(Farm, slug=slug)
    context = {
        'farm': farm,
        'payment_amount': 600,
        'payment_number': '4522546',
        'payment_name': 'Alvin',
    }
    return render(request, 'mashamba/dairyfarm/pay_to_activate.html', context)


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

    # Retrieve products_services related to the farm
    products_services = farm.products_services.all()

    context = {
        'farm': farm,
        'products_services': products_services,
        'email': farm.email,
        'phone_number': farm.phone_number,
    }

    return render(request, 'mashamba/dairyfarm/farm_detail.html', context)


@login_required
def add_cow_view(request, slug):
    farm = get_object_or_404(Farm, slug=slug, manager=request.user)

    if request.method == 'POST':
        form = CowForm(request.POST)
        if form.is_valid():
            cow = form.save(commit=False)
            cow.farm = farm  # Ensure farm is assigned before saving
            cow.save()
            return redirect('mashamba:cow_list', slug=farm.slug)
    else:
        form = CowForm()

    context = {
        'form': form,
        'farm': farm,
    }
    return render(request, 'mashamba/dairyfarm/add_cow.html', context)


@login_required
def cow_list_view(request, slug):
    user = request.user
    farm = get_object_or_404(Farm, slug=slug, manager=user)
    cows = Cow.objects.filter(farm=farm)

    # Pagination
    paginator = Paginator(cows, 7)  # Show 10 cows per page
    page = request.GET.get('page')

    try:
        cows_paginated = paginator.page(page)
    except PageNotAnInteger:
        cows_paginated = paginator.page(1)
    except EmptyPage:
        cows_paginated = paginator.page(paginator.num_pages)

    context = {
        'farm': farm,
        'cows': cows_paginated,  # Pass paginated cows to the template
    }
    return render(request, 'mashamba/dairyfarm/cow_list.html', context)

@login_required
def cow_detail_view(request, slug, cow_id):
    user = request.user
    farm = get_object_or_404(Farm, slug=slug, manager=user)  # Ensure user owns the farm
    cow = get_object_or_404(Cow, id=cow_id, farm=farm)
    #last_mass = cow.mass_measurements.order_by('-date_measured').first()

    context = {
        'farm': farm,
        'cow': cow,
        #'last_mass': last_mass
    }
    return render(request, 'mashamba/dairyfarm/cow_detail.html', context)



@login_required
def add_milking_session_view(request, slug, cow_id):
    farm = get_object_or_404(Farm, slug=slug, manager=request.user)
    cow = get_object_or_404(Cow, id=cow_id, farm=farm)

    if request.method == 'POST':
        form = MilkingSessionForm(request.POST)
        if form.is_valid():
            milking_session = form.save(commit=False)
            milking_session.cow = cow
            # Assign milking_time from the form data
            milking_session.milking_time = form.cleaned_data['milking_time']
            milking_session.save()
            return redirect('mashamba:milking_sessions', slug=farm.slug, cow_id=cow.id)
    else:
        form = MilkingSessionForm()

    context = {
        'form': form,
        'farm': farm,
        'cow': cow,
    }
    return render(request, 'mashamba/dairyfarm/add_milking_session.html', context)


@login_required
def milking_sessions_view(request, slug, cow_id):
    user = request.user
    farm = get_object_or_404(Farm, slug=slug, manager=user)  # Ensure user owns the farm
    cow = get_object_or_404(Cow, id=cow_id, farm=farm)

    milking_sessions = MilkingSession.objects.filter(cow=cow).order_by('milking_time')
    grouped_milk_yield = {}

    for session in milking_sessions:
        date = session.milking_time.date()
        if date not in grouped_milk_yield:
            grouped_milk_yield[date] = {'sessions': [], 'total': 0}
        grouped_milk_yield[date]['sessions'].append(session)
        grouped_milk_yield[date]['total'] += session.milk_yield

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

    # Aggregate milking sessions by cow and date
    milking_sessions = MilkingSession.objects.filter(cow__farm=farm).values(
        'cow__name_or_tag', 'milking_time__date'
    ).annotate(total_yield=Sum('milk_yield')).order_by('-milking_time__date', 'cow__name_or_tag')

    # Group by date
    grouped_milk_yield = defaultdict(list)
    for session in milking_sessions:
        date_str = session['milking_time__date'].strftime("%Y-%m-%d")
        grouped_milk_yield[date_str].append({
            'cow': session['cow__name_or_tag'],
            'total_yield': session['total_yield']
        })

    # Sort dates in descending order
    sorted_grouped_milk_yield = sorted(grouped_milk_yield.items(), reverse=True)

    # Prepare context to pass data to the template
    context = {
        'farm': farm,
        'sorted_grouped_milk_yield': sorted_grouped_milk_yield,
    }

    return render(request, 'mashamba/dairyfarm/all_cows_milk.html', context)
