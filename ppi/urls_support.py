from django.urls import path

from ticket import views as ticket_views

urlpatterns = [
    path('', ticket_views.CustomIndex.as_view(), name='index'),
]
