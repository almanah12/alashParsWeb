from django.shortcuts import render
from .models import TempTable


def main(request):
    return render(request, 'scrap/main.html')


def table_view(request):
    info = TempTable.objects.all()
    return render(request, 'scrap/temp_table.html', context={'info': info})
