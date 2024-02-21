# button_app/urls.py
'''from django.urls import path
from .views import button_view

urlpatterns = [
    path('', button_view, name='button_page'),
]
from .views import process_input

urlpatterns = [
    path('input/', process_input, name='process_input'),
]'''
from django.urls import path
from django.views.generic import RedirectView

from gdsc.views import process_input

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='process_input', permanent=False)),
    path('input/', process_input, name='process_input'),
    path('process/', process_input, name='input_page'),
    # Other URL patterns for your project...
]
