from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.http import HttpResponseRedirect, HttpResponseNotFound

from .forms import WeightForm
from .models import Weight

def index(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.user.is_authenticated:
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
    return render(request, 'app_weight/index.html', {'form': WeightForm()})
