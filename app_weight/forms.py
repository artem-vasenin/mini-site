from django.forms import Form, DateField, IntegerField, CharField, DateInput, NumberInput, TextInput
from app_weight.models import Weight

class WeightForm(Form):
    date = DateField(
        widget=DateInput(attrs={'class': 'datepicker'}),
        label='Дата',
    )
    morning = IntegerField(
        widget=NumberInput(attrs={'class': 'number'}),
        label='Утро',
        required=False,
    )
    evening = IntegerField(
        widget=NumberInput(attrs={'class': 'number'}),
        label='Вечер',
        required=False,
    )
    comment=CharField(
        widget=TextInput(attrs={'class': 'text'}),
        max_length=255,
        required=False,
    )
