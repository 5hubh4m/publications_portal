from django.conf.urls import url

from . import views

app_name = 'portal'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^publication/(?P<publication_id>[0-9]+)/$', views.publication, name='publication'),
    url(r'^institute/(?P<institute_id>[0-9]+)/$', views.institute, name='institute'),
    url(r'^department/(?P<department_id>[0-9]+)/$', views.department, name='department'),
    url(r'^field/(?P<field_id>[0-9]+)/$', views.field, name='field'),
    url(r'^author/(?P<author_id>[0-9]+)/$', views.author, name='author'),
    url(r'^publisher/(?P<publisher_id>[0-9]+)/$', views.publisher, name='publisher'),
    url(r'^dump/$', views.dump, name='dump'),
    url(r'^404/$', views.not_found, name='404')
]