from django.urls import path
from .views import home, worldwide, measures

app_name = 'corona_app'

urlpatterns = [
    path('', home, name='home-page'),
    path('worldwide/', worldwide, name='worldwide-page'),
    path('preventive-measures/', measures, name='preventive-measures-page'),
]