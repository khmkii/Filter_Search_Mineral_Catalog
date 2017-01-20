from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'(?P<pk>\d+)', views.one_mineral, name='see_mineral'),
    url(r'search/.*', views.search, name='search'),
    url(r'random', views.random_mineral, name='random_mineral'),
    url(r'starts_with/(?P<start_letter>\w)', views.first_letter, name='first_letter'),
    url(r'^$', views.home, name='home'),
    url(r'group/(?P<grouping>\w+)', views.group_minerals, name='groups'),
    url(r'streak/(?P<streak_color>\w+)', views.streak_minerals, name='streaks')
]