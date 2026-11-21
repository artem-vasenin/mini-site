import csv
import io
from datetime import datetime
from urllib import response

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required

from .forms import WeightForm, FileForm
from .models import Weight

months = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь',
]

@login_required
def index(request: HttpRequest) -> HttpResponse:
    lst = Weight.objects.all().filter(user=request.user).order_by('-date', )
    result = {}
    for w in lst:
        y = w.date.year
        m = months[w.date.month-1]
        d = w.date.day
        result.setdefault(y, {}).setdefault(m, {})[d] = {
            "id": w.id,
            "morning": w.morning,
            "evening": w.evening,
            "comment": w.comment,
        }
    return render(request, 'app_weight/index.html', {'data': result})

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
    ctx = {
        'form': FileForm(),
        'parsed_cnt': None,
        'errors_cnt': None,
        'errors': None,
    }
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data['data']
            text = io.TextIOWrapper(data.file, encoding="utf-8-sig", newline="")
            reader = csv.DictReader(text, delimiter=';')
            parsed_cnt = 0
            errors = {}
            for r in reader:
                try:
                    date = datetime.strptime(r['date'], '%Y-%m-%d').date()
                    morning = float(r['morning']) if r['morning'] else None
                    evening = float(r['evening']) if r['evening'] else None
                    comment = r['comment'] if r['comment'] else None
                    Weight.objects.update_or_create(
                        user=request.user,
                        date=date,
                        defaults={
                            'morning': morning,
                            'evening': evening,
                            'comment': comment,
                        },
                    )
                    parsed_cnt += 1
                except Exception as e:
                    errors[r['date']] = e
                    continue
            ctx['parsed_cnt'] = parsed_cnt
            ctx['errors_cnt'] = len(errors)
            ctx['errors'] = errors
            return render(
                request,
                'app_weight/file.html',
                ctx
            )

    return render(
        request,
        'app_weight/file.html',
        ctx
    )

@login_required
def edit(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        w = Weight.objects.get(pk=pk)
    except Weight.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == 'POST':
        form = WeightForm(request.POST)
        if form.is_valid():
            w.morning = form.cleaned_data['morning']
            w.evening = form.cleaned_data['evening']
            w.comment = form.cleaned_data['comment']
            w.save()
        return HttpResponseRedirect('/weight/')
    return render(
        request,
        'app_weight/create.html',
        {'form': WeightForm(initial={
            'date': w.date,
            'morning': w.morning,
            'evening': w.evening,
            'comment': w.comment,
        })},
    )

@login_required
def delete(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        w = Weight.objects.get(pk=pk)
    except Weight.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == 'POST':
        w.delete()
        return HttpResponseRedirect('/weight/')
    return render(request, 'app_weight/delete.html', {'data': w})

@login_required
def export(request: HttpRequest) -> HttpResponse:
    lst = Weight.objects.all().filter(user=request.user).order_by('-date')
    response = HttpResponse(
        content_type="text/csv; charset=utf-8",
    )
    response["Content-Disposition"] = (
        'attachment; filename="weight.csv"'
    )
    response.write("\ufeff")
    writer = csv.writer(response, delimiter=";")
    writer.writerow([
        "date", "morning", "evening", "comment"
    ])

    for w in lst:
        writer.writerow([
            w.date.isoformat(),
            w.morning or '',
            w.evening or '',
            w.comment or '',
        ])

    return response

