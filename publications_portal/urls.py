"""publications_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import (
    login,
    logout,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete
)

urlpatterns = [
    url(r'^', include('portal.urls')),
    url(r'^', include('accounts.urls')),
    url(r'^login/$', login,
        {
            'template_name': 'accounts/login.html'
        },
        name='login'),
    url(r'^logout/$', logout,
        {
            'next_page': '/login'
        },
        name='logout'),
    url(r'^password_reset/$', password_reset,
        {
            'template_name': 'accounts/password_reset.html',
            'post_reset_redirect': '/password_reset/done',
        },
        name='password_reset'),
    url(r'^password_reset/done$', password_reset_done,
        {
            'template_name': 'accounts/password_reset_done.html'
        },
        name='password_reset_done'),
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,
        {
            'template_name': 'accounts/password_reset_confirm.html',
            'post_reset_redirect': '/password_reset/complete',
        },
        name='password_reset_confirm'),
    url(r'^password_reset/complete/$', password_reset_complete,
        {
            'template_name': 'accounts/password_reset_complete.html'
        },
        name='password_reset_complete'),
    url(r'^admin/', admin.site.urls),
    url(r'^add/', include('creator.urls'))
]
