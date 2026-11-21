import csv
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
            user = request.user
            w = Weight()
            w.date = form.cleaned_data['date']
            w.morning = form.cleaned_data['morning']
            w.evening = form.cleaned_data['evening']
            w.comment = form.cleaned_data['comment']
            w.user = user
            w.save()
        return HttpResponseRedirect('/weight/')
    return render(request, 'app_weight/create.html', {'form': WeightForm()})

@login_required
def file(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data['data']
            print(data.name)
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
