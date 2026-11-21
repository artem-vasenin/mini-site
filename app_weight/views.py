import csv
import io
from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required

from .forms import WeightForm, FileForm
from .models import Weight

@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'app_weight/index.html')

@login_required
def create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = WeightForm(request.POST)
        if form.is_valid():
            _, _created = Weight.objects.update_or_create(
                user=request.user,
                date=form.cleaned_data['date'],
                defaults={
                    'morning': form.cleaned_data['morning'],
                    'evening': form.cleaned_data['evening'],
                    'comment': form.cleaned_data['comment'],
                },
            )
        return HttpResponseRedirect('/weight/')
    return render(request, 'app_weight/create.html', {'form': WeightForm()})

@login_required
def file(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data['data']
            text = io.TextIOWrapper(data.file, encoding="utf-8-sig", newline="")
            reader = csv.DictReader(text, delimiter=';')
            for r in reader:
                date = datetime.strptime(r['date'], '%Y-%m-%d').date()
                morning = float(r['morning']) if r['morning'] else None
                evening = float(r['evening']) if r['evening'] else None
                comment = r['comment'] if r['comment'] else None
                print(date, morning, evening, comment)
    return render(
        request,
        'app_weight/file.html',
        { 'form': FileForm() }
    )

@login_required
def edit(request: HttpRequest, pk: int) -> HttpResponse:
    return render(
        request,
        'app_weight/edit.html',
        {'pk': pk}
    )
