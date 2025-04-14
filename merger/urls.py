from django.urls import path
from . import views

urlpatterns = [
    path('', views.merge_pdfs, name='merge_pdfs'),
]
