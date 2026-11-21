import csv
import io
from pathlib import Path
from django.utils import timezone
from django.core.exceptions import ValidationError

from django.forms import (
    Form, DateField, FloatField, CharField, DateInput, NumberInput, TextInput,
    FileField, ClearableFileInput,
)

class WeightForm(Form):
    date = DateField(
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date', 'class': 'form-control'}
        ),
        initial=timezone.localdate,
        label='Дата',
    )
    morning = FloatField(
        widget=NumberInput(attrs={'class': 'form-control'}),
        label='Утро',
        required=False,
    )
    evening = FloatField(
        widget=NumberInput(attrs={'class': 'form-control'}),
        label='Вечер',
        required=False,
    )
    comment=CharField(
        widget=TextInput(attrs={'class': 'form-control'}),
        max_length=255,
        required=False,
    )

class FileForm(Form):
    data = FileField(
        widget=ClearableFileInput(
            attrs={
                "class": "form-control",
                "accept": ".csv,text/csv",
            }
        ),
        label="Файл данных",
    )

    def clean_data(self):
        file = self.cleaned_data["data"]

        if Path(file.name).suffix.lower() != ".csv":
            raise ValidationError("Файл должен иметь расширение .csv")

        if file.size > 1024 * 1024:
            raise ValidationError("Размер файла не должен превышать 1 МБ")

        try:
            content = file.read().decode("utf-8-sig")
            reader = csv.DictReader(
                io.StringIO(content),
                delimiter=";",
                strict=True,
            )

            if reader.fieldnames != [
                "date", "morning", "evening", "comment"
            ]:
                raise ValidationError(
                    "Неверный формат CSV. Ожидаются поля: "
                    "date;morning;evening;comment"
                )

            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    raise ValidationError(
                        "Некорректное количество столбцов в CSV."
                    )

        except (UnicodeDecodeError, csv.Error) as exc:
            raise ValidationError(
                "Не удалось прочитать CSV-файл в кодировке UTF-8."
            ) from exc

        finally:
            file.seek(0)

        return file
