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
    url(r'^home/', home),
    url(r'^manage/', manage),
    url(r'^account/', account),
    url(r'^contact/', contact),
    url(r'^remove/(?P<task_id>.+)/(?P<course_name>.+)', remove),
    url(r'^courses/(?P<subject_name>.+)/(?P<abbrev>.+)', courses),
    url(r'^sections/(?P<course_name>.+)/(?P<abbrev>.+)/(?P<subject_name>.+)', sections),
    url(r'^scan/(?P<abbrev>.+)/(?P<course_name>.+)/(?P<subject_name>.+)', scan),
    url(r'^register/success', register_success),
    url(r'^register/', register),
    url(r'^logout/', logout_page),
    # url(r'^accounts/', include('registration.backends.simple.urls')),
]
