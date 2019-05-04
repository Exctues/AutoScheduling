from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.model_form_upload, name='upload'),
    path('schedule/<int:number>/', views.show_schedule_view, name='schedule'),
    path('download_uploaded/<int:number>/', views.downloadUploadedCsv, name='download_uploaded'),
    path('download/<int:number>/', views.downloadSchedule, name='download_generated'),
    path('uploaded/', views.uploadedHisotry, name='uploaded'),
    path('uploaded/<int:schnum>/<int:time>/', views.schedule_generate, name='generate_schedule'),
    path('save_schedule/<int:number>/', views.save_schedule, name='save schedule'),
    path('history/', views.scheduleHistory, name='history'),
    path('edit/<int:number>/', views.edit_schedule, name='edit')
    # path('csv/', views.print_csv_file, name='print_csv_file'),
]
