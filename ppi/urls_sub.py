from django.urls import path

from ticket import views as ticket_views

urlpatterns = [
    path('', ticket_views.SubDomainIndex.as_view(), name='index'),
]
