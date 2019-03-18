from django.shortcuts import render
from u_csv.forms import DocumentForm
from django.shortcuts import redirect
from .Parser import Data
import os
from CATt import settings
from .Parser.Common import nl


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('csv/')
    else:
        form = DocumentForm()
    return render(request, 'upload_form.html', {
        'form': form
    })


def print_csv_file(request):
    ans = str(Data.getScheduleData(os.path.join(settings.BASE_DIR, 'files/Sample_Data.csv'))).split(nl)
    #ans = Parser.parse(os.path.join(settings.BASE_DIR, 'files/Sample_Data.csv'))
    return render(request, 'print_csv.html', {
        'ans': ans
    })
