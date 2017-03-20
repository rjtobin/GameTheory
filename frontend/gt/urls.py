from django.conf.urls import url

from . import views

app_name = 'gt'

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<problem_id>[0-9]+)/$', views.problem, name='problem'),
    url(r'^upload/', views.upload, name='upload'),
]

