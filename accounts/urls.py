from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^dashboard/$', views.DashBoard.as_view(), name='dashboard'),
    url(r'^signup/$', views.RegistrationView.as_view(),
        {
            'template_name': 'accounts/signup.html',
            'next_page': '/password_reset'
        },
        name='signup'),
    url(r'^signup/successful/$', views.successful),
    url(r'^approve/(?P<publication_id>[0-9]+)$', views.approve, name='approve')
]
