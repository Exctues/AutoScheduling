from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', views.model_form_upload, name='upload'),
    path('csv/', views.print_csv_file, name='print_csv_file'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR)

