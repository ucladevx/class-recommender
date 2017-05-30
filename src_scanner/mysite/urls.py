"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from scanner.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login),
    url(r'^account/edit', edit),
    url(r'^account/', account),
    url(r'^contact/', contact),

    url(r'^scanner1', scanner1),
    url(r'^scanner2', scanner2),
    url(r'^classes/(?P<term>.+)/(?P<subject>.+)', get_classes),
    url(r'^overview/(?P<term>.+)/(?P<course>.+)', get_overview),


    url(r'^home/(?P<term>.+)', home),
    url(r'^courses/(?P<term>.+)/(?P<subject>.+)', courses),
    url(r'^sections/(?P<term>.+)/(?P<course>.+)/(?P<check>.+)', sections),
    url(r'^scan/(?P<term>.+)/(?P<course>.+)', scan),

    url(r'^manage/', manage),
    url(r'^remove/(?P<course>.+)', remove),

    url(r'^register/success', register_success),
    url(r'^register/', register),
    url(r'^logout/', logout_page),
    url('^', include('django.contrib.auth.urls')),
]
