from user import views as user_views

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from ticket import views as ticket_views

urlpatterns = [
    path('', ticket_views.Tickets.as_view(), name='index'),

    path('login/', user_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^signup/$', user_views.SignUp.as_view(), name='signup'),

    url(r'^profile/$', user_views.SignUp.as_view(), name='profile'),

    url(r'^tickets/$', ticket_views.Tickets.as_view(), name='tickets'),
    url(r'^tickets/create/$', ticket_views.CreateTicket.as_view(), name='ticket_create'),
    url(r'^tickets/(?P<slug>[0-9A-Za-z_\-]+)/$', ticket_views.ViewTicket.as_view(), name='ticket_detail'),
    url(r'^tickets/(?P<slug>[0-9A-Za-z_\-]+)/pay/$', ticket_views.PayTicket.as_view(), name='ticket_pay'),
    url(r'^tickets/(?P<slug>[0-9A-Za-z_\-]+)/edit/$', ticket_views.UpdateTicket.as_view(), name='ticket_edit'),
    url(r'^tickets/<int:pk>/$', ticket_views.ViewTicket.as_view(), name='ticket_detail_pk'),

    url(r'^paypal/', include('paypal.standard.ipn.urls')),

    path('admin/', admin.site.urls),
]


handler404 = 'ppi.handlers.handler404'


if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
