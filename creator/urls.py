from django.conf.urls import url

from . import views

app_name = 'creator'
urlpatterns = [
    url('^author/$', views.AddAuthor.as_view(), name='author'),
    url('^institute/$', views.AddInstitute.as_view(), name='institute'),
    url('^department/$', views.AddDepartment.as_view(), name='department'),
    url('^field/$', views.AddField.as_view(), name='field'),
    url('^publisher/$', views.AddPublisher.as_view(), name='publisher'),
    url('^successful/$', views.action_successful, name='successful'),
    url('^publication/$', views.AddPublication.as_view(), name='publication'),
]