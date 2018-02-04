from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('monitor/<str:address>', views.monitor, name='monitor'),
    path('chart_data_json/<str:addr>/<int:pool>', views.chart_data_json, name='chart_data_json'),
]
