from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('monitor/<str:address>', views.monitor, name='monitor'),
    path('monitor/<str:address>/<int:pool_id>', views.monitor_pool, name='monitor_pool'),
    path('chart_data_json/<str:addr>/<int:pool_id>', views.chart_data_json, name='chart_data_json'),
]
